import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"FRED Macro Agent","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/fred-macro-agent.md","filePath":"concepts/fred-macro-agent.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "concepts/fred-macro-agent.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="fred-macro-agent" tabindex="-1">FRED Macro Agent <a class="header-anchor" href="#fred-macro-agent" aria-label="Permalink to &quot;FRED Macro Agent&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>The Macro Analysis Agent loads macroeconomic time series from FRED or deterministic sample data, summarizes recent observations, and cites the series used.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>Company risk often depends on macro context. Interest rates, inflation, unemployment, GDP, and treasury yields can all affect valuation, demand, and investor sentiment.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ul><li>Supported series include <code>FEDFUNDS</code>, <code>CPIAUCSL</code>, <code>UNRATE</code>, <code>GDP</code>, and <code>DGS10</code>.</li><li>The service uses FRED when <code>FRED_API_KEY</code> is configured.</li><li>Sample fallback keeps local demos and tests stable.</li><li>Observations are cached in PostgreSQL.</li><li>Macro questions route to <code>macro-analysis-agent</code>.</li><li>Company-plus-macro questions can route to <code>macro-document-orchestrator</code>.</li></ul><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Deterministic summaries avoid extra LLM cost.</li><li>Sample fallback improves demo reliability.</li><li>The current trend logic is simple and explainable.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>FRED API key missing.</li><li>Series unavailable.</li><li>Cached data stale.</li><li>Macro context overgeneralized without company-specific evidence.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>The macro agent demonstrates multi-source reasoning: a user can combine external economic indicators with company disclosures.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/fred-macro-agent.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const fredMacroAgent = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  fredMacroAgent as default
};
