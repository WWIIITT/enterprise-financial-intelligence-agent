import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Evaluation Engine","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/evaluation-engine.md","filePath":"concepts/evaluation-engine.md","lastUpdated":null}');
const _sfc_main = { name: "concepts/evaluation-engine.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="evaluation-engine" tabindex="-1">Evaluation Engine <a class="header-anchor" href="#evaluation-engine" aria-label="Permalink to &quot;Evaluation Engine&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>The Evaluation Engine runs deterministic test cases against chat and endpoint behavior, then scores route accuracy, source coverage, citations, answer terms, latency, and hallucination-risk flags.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>Enterprise AI needs quality tracking. Manual demos are not enough to show reliability.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ul><li>JSON fixtures define expected agents, sources, citations, and answer terms.</li><li><code>/api/evals/run</code> executes a suite.</li><li><code>/api/evals/report</code> writes markdown and JSON reports.</li><li>Evaluation run records are stored in PostgreSQL.</li></ul><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Deterministic checks are repeatable and low cost.</li><li>They are a proxy for semantic quality, not a full human review.</li><li>LLM-as-judge can be added later when cost and variance are acceptable.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>Tests can become too brittle.</li><li>Required terms may miss valid paraphrases.</li><li>Passing smoke tests does not guarantee full production quality.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>The evaluation system shows that each agent route is measurable. It gives concrete quality evidence instead of relying on subjective demos.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/evaluation-engine.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const evaluationEngine = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  evaluationEngine as default
};
