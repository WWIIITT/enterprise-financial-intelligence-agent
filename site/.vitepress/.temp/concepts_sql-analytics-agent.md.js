import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"SQL Analytics Agent","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/sql-analytics-agent.md","filePath":"concepts/sql-analytics-agent.md","lastUpdated":null}');
const _sfc_main = { name: "concepts/sql-analytics-agent.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="sql-analytics-agent" tabindex="-1">SQL Analytics Agent <a class="header-anchor" href="#sql-analytics-agent" aria-label="Permalink to &quot;SQL Analytics Agent&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>The SQL Analytics Agent answers structured financial metric questions using safe query templates over PostgreSQL financial facts.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>Some questions should not use RAG. Revenue trends and balance-sheet values are structured data problems and should be answered with controlled queries.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ul><li>SEC Company Facts are ingested into PostgreSQL.</li><li>Supported metrics map to predefined concepts.</li><li><code>/api/sql/analyze</code> accepts ticker, metric, period, and limit.</li><li>Raw SQL input is never accepted.</li><li>Chat questions with metric intent route to <code>sql-analytics-agent</code>.</li></ul><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Safe templates reduce injection risk.</li><li>Deterministic analytics are easier to test.</li><li>The approach supports fewer free-form questions than LLM-generated SQL.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>Unsupported metric.</li><li>Missing company facts.</li><li>Duplicate SEC facts for the same fiscal year.</li><li>Concept mapping differs across companies.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>The important design choice is not just adding SQL. It is adding SQL safely, without letting the model generate arbitrary queries.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/sql-analytics-agent.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const sqlAnalyticsAgent = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  sqlAnalyticsAgent as default
};
