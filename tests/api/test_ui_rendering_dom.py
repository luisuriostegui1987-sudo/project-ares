"""XSS regression — executes the ACTUAL served rendering path.

The page script is extracted verbatim from the asset served by the real API
(GET /) and executed under Node against an instrumented DOM stub that records
every element and attribute the product code creates. A report whose fields
all carry a malicious payload is rendered through the real renderReport().

Proven per payload:
- no <script> element is created;
- no <img> element is created from injected content;
- no event-handler attribute (on*) is created;
- no attribute value carries the payload;
- the payload appears ONLY as literal text.

Skipped when Node is unavailable (local dev boxes); always runs in CI
(ubuntu runners ship Node).
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest
from fastapi.testclient import TestClient
from test_ui_security import XSS_PAYLOADS, _report_with_payload

from ares.api import create_app
from ares.reports import InMemoryReportStore
from ares.service import ResearchService

NODE = shutil.which("node")

_HARNESS = r"""
class StubNode {
  constructor(tag) {
    this.tagName = String(tag || "").toUpperCase();
    this.children = []; this.attributes = {}; this._text = "";
    this.className = ""; this.hidden = false; this.dataset = {};
  }
  set textContent(v) { this._text = String(v); this.children = []; }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join("");
  }
  appendChild(c) { this.children.push(c); return c; }
  append(...cs) { cs.forEach((c) => this.appendChild(c)); }
  replaceChildren(...cs) { this.children = []; cs.forEach((c) => this.appendChild(c)); }
  setAttribute(k, v) { this.attributes[String(k)] = String(v); }
  addEventListener() {}
  set colSpan(v) { this.attributes["colspan"] = String(v); }
  set onsubmit(v) {} set onclick(v) {}
}
class StubText {
  constructor(t) { this.tagName = "#text"; this._text = String(t); this.children = []; }
  get textContent() { return this._text; }
}
globalThis.HTMLElement = StubNode;
const registry = {};
globalThis.document = {
  createElement: (t) => new StubNode(t),
  createTextNode: (t) => new StubText(t),
  getElementById: (id) => registry[id] || (registry[id] = new StubNode("div")),
  querySelectorAll: () => [],
};
globalThis.fetch = async () => ({ ok: true, status: 200, json: async () => [] });

/* __PAGE_SCRIPT__ */

const report = JSON.parse(process.argv[1]);
renderReport(report);

const all = [];
(function walk(n) { all.push(n); (n.children || []).forEach(walk); })(
  { children: Object.values(registry) }
);
const dangerous = all.filter((n) => n.tagName === "SCRIPT" || n.tagName === "IMG");
const handlerAttrs = all.filter((n) =>
  Object.keys(n.attributes || {}).some((k) => k.toLowerCase().startsWith("on"))
);
const payloadInAttrs = all.filter((n) =>
  Object.values(n.attributes || {}).some((v) => String(v).includes("alert(1)"))
);
const renderedText = registry["report-card"]
  ? Object.values(registry).map((n) => n.textContent).join("\n")
  : "";
console.log(JSON.stringify({
  dangerousElements: dangerous.map((n) => n.tagName),
  handlerAttrs: handlerAttrs.length,
  payloadInAttrs: payloadInAttrs.length,
  payloadIsLiteralText: renderedText.includes(process.argv[2]),
}));
"""


def _served_page_script() -> str:
    client = TestClient(create_app(ResearchService(reports=InMemoryReportStore())))
    html = client.get("/").text
    return html.split("<script>")[1].split("</script>")[0]


@pytest.mark.skipif(NODE is None, reason="Node runtime required (present in CI)")
@pytest.mark.parametrize("payload", XSS_PAYLOADS)
def test_real_rendering_path_renders_payloads_as_literal_text(payload: str) -> None:
    report = json.loads(_report_with_payload(payload).model_dump_json())
    # Exercise EVERY dynamic section: inject the payload into a synthetic fact
    # row and signal row as rendered dicts (rendering-path test, not a model test).
    report["facts"] = [
        {
            "metric_name": payload,
            "value": payload,
            "unit": payload,
            "knowledge_class": payload,
            "source_name": payload,
        }
    ]
    report["signals"] = [
        {
            "signal_type": payload,
            "measured_value": payload,
            "direction": payload,
            "rule_version": payload,
        }
    ]
    harness = _HARNESS.replace("/* __PAGE_SCRIPT__ */", _served_page_script())
    result = subprocess.run(
        [NODE or "node", "-e", harness, json.dumps(report), payload],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, f"node harness failed: {result.stderr}"
    verdict = json.loads(result.stdout.strip().splitlines()[-1])
    assert verdict["dangerousElements"] == []  # no <script>, no <img> created
    assert verdict["handlerAttrs"] == 0  # no on* attributes created
    assert verdict["payloadInAttrs"] == 0  # payload never lands in an attribute
    assert verdict["payloadIsLiteralText"] is True  # rendered as literal text
