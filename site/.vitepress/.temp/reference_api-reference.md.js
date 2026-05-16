import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"API Reference","description":"","frontmatter":{},"headers":[],"relativePath":"reference/api-reference.md","filePath":"reference/api-reference.md","lastUpdated":null}');
const _sfc_main = { name: "reference/api-reference.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="api-reference" tabindex="-1">API Reference <a class="header-anchor" href="#api-reference" aria-label="Permalink to &quot;API Reference&quot;">​</a></h1><h2 id="core" tabindex="-1">Core <a class="header-anchor" href="#core" aria-label="Permalink to &quot;Core&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Method</th><th>Path</th><th>Purpose</th></tr></thead><tbody><tr><td><code>GET</code></td><td><code>/health</code></td><td>Service health check</td></tr><tr><td><code>GET</code></td><td><code>/api/config/status</code></td><td>Environment and service readiness</td></tr><tr><td><code>POST</code></td><td><code>/api/chat</code></td><td>Main agent workflow</td></tr></tbody></table><h2 id="ingestion" tabindex="-1">Ingestion <a class="header-anchor" href="#ingestion" aria-label="Permalink to &quot;Ingestion&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Method</th><th>Path</th><th>Purpose</th></tr></thead><tbody><tr><td><code>POST</code></td><td><code>/api/ingest/policy</code></td><td>Index internal policy documents</td></tr><tr><td><code>POST</code></td><td><code>/api/ingest/sec</code></td><td>Index sample or live SEC filings</td></tr><tr><td><code>POST</code></td><td><code>/api/ingest/company-facts</code></td><td>Index SEC Company Facts into PostgreSQL</td></tr></tbody></table><h2 id="analysis" tabindex="-1">Analysis <a class="header-anchor" href="#analysis" aria-label="Permalink to &quot;Analysis&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Method</th><th>Path</th><th>Purpose</th></tr></thead><tbody><tr><td><code>GET</code></td><td><code>/api/macro/series/{series_id}</code></td><td>Load macro series observations</td></tr><tr><td><code>POST</code></td><td><code>/api/macro/analyze</code></td><td>Analyze macro context</td></tr><tr><td><code>POST</code></td><td><code>/api/sql/analyze</code></td><td>Analyze structured financial metrics</td></tr></tbody></table><h2 id="governance-and-operations" tabindex="-1">Governance And Operations <a class="header-anchor" href="#governance-and-operations" aria-label="Permalink to &quot;Governance And Operations&quot;">​</a></h2><table tabindex="0"><thead><tr><th>Method</th><th>Path</th><th>Purpose</th></tr></thead><tbody><tr><td><code>POST</code></td><td><code>/api/security/check</code></td><td>Run deterministic security checks</td></tr><tr><td><code>POST</code></td><td><code>/api/evals/run</code></td><td>Run an evaluation suite</td></tr><tr><td><code>POST</code></td><td><code>/api/evals/report</code></td><td>Generate evaluation report</td></tr><tr><td><code>GET</code></td><td><code>/api/observability/summary</code></td><td>Load operational dashboard summary</td></tr></tbody></table></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("reference/api-reference.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const apiReference = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  apiReference as default
};
