import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"RAG And Citations","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/rag-and-citations.md","filePath":"concepts/rag-and-citations.md","lastUpdated":null}');
const _sfc_main = { name: "concepts/rag-and-citations.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="rag-and-citations" tabindex="-1">RAG And Citations <a class="header-anchor" href="#rag-and-citations" aria-label="Permalink to &quot;RAG And Citations&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>Retrieval-Augmented Generation, or RAG, answers a question by retrieving relevant source text before composing a response. In Aurelia Ledger, RAG is citation-aware: answers must expose the source chunks used as evidence.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>Financial and compliance answers need evidence. A useful answer is not only fluent; it must point back to SEC filings or internal policy documents.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ol><li>Documents are cleaned and chunked.</li><li>Chunks are embedded and indexed in Qdrant.</li><li>User questions are embedded.</li><li>Qdrant retrieves candidate chunks.</li><li>Lightweight reranking and confidence checks filter weak evidence.</li><li>The response includes answer text, source list, trace, and metrics.</li></ol><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Deterministic synthesis keeps cost low and reduces hallucination risk.</li><li>Citation formatting is easier to evaluate than free-form long answers.</li><li>Retrieval quality depends on chunking, embeddings, and reranking.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>Weak retrieval can surface unrelated policy chunks.</li><li>Overly large chunks can dilute evidence.</li><li>Overly small chunks can lose context.</li><li>Missing citations reduce trust even when the answer is correct.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>The project treats citations as a product requirement, not a cosmetic detail. In finance, the user needs to know which document supports each claim.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/rag-and-citations.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const ragAndCitations = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  ragAndCitations as default
};
