import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Observability Dashboard","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/observability-dashboard.md","filePath":"concepts/observability-dashboard.md","lastUpdated":null}');
const _sfc_main = { name: "concepts/observability-dashboard.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="observability-dashboard" tabindex="-1">Observability Dashboard <a class="header-anchor" href="#observability-dashboard" aria-label="Permalink to &quot;Observability Dashboard&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>The Observability Dashboard summarizes operational data from request logs, evaluation runs, and security audits.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>Operators need to know which agents are used, how long requests take, whether evaluations are passing, and how often security guardrails trigger.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ul><li>Request logs track selected agent, latency, sources count, and estimated cost.</li><li>Evaluation runs track suite results.</li><li>Security audits track risk level and action.</li><li><code>/api/observability/summary</code> aggregates the latest state.</li><li>The React dashboard displays compact metrics and distributions.</li></ul><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Custom PostgreSQL observability is simple and portfolio-friendly.</li><li>Prometheus and Grafana would be stronger for production.</li><li>Empty database states return stable summaries instead of failing.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>PostgreSQL logs are not a full metrics backend.</li><li>Long-term retention policy is not implemented.</li><li>High-cardinality metrics need careful production design.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>Observability turns the project from a chatbot into an operable system. It shows what happened, not just what the user saw.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/observability-dashboard.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const observabilityDashboard = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  observabilityDashboard as default
};
