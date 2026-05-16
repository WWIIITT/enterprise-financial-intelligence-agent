import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"LangGraph Orchestrator","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/langgraph-orchestrator.md","filePath":"concepts/langgraph-orchestrator.md","lastUpdated":null}');
const _sfc_main = { name: "concepts/langgraph-orchestrator.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="langgraph-orchestrator" tabindex="-1">LangGraph Orchestrator <a class="header-anchor" href="#langgraph-orchestrator" aria-label="Permalink to &quot;LangGraph Orchestrator&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>The LangGraph Orchestrator is the workflow layer behind <code>/api/chat</code>. It decides which agent path should handle a question and assembles traceable response steps.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>The platform has multiple agents and tools. Routing logic must be explicit, testable, and visible in traces.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ul><li>Security preflight runs before the graph.</li><li>Deterministic router selects policy, document, macro, macro-document, SQL, or fallback.</li><li>Agent nodes call existing services.</li><li>Response shape remains stable for the frontend.</li></ul><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Deterministic routing is cheaper and easier to evaluate than LLM routing.</li><li>Rule-based routing can miss unusual phrasing.</li><li>Keeping the public API stable protects the frontend from backend refactors.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>Ambiguous questions may route to the wrong agent.</li><li>Multi-agent synthesis can become too broad.</li><li>Routing rules must evolve with new agent capabilities.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>LangGraph is used for workflow clarity, not for hype. It makes route decisions and trace steps explicit.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/langgraph-orchestrator.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const langgraphOrchestrator = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  langgraphOrchestrator as default
};
