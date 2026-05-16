import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Qdrant Vector Retrieval","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/qdrant-vector-retrieval.md","filePath":"concepts/qdrant-vector-retrieval.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "concepts/qdrant-vector-retrieval.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="qdrant-vector-retrieval" tabindex="-1">Qdrant Vector Retrieval <a class="header-anchor" href="#qdrant-vector-retrieval" aria-label="Permalink to &quot;Qdrant Vector Retrieval&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>Qdrant is the vector database used to store embedded document chunks and retrieve semantically similar chunks for a query.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>The platform needs persistent retrieval across backend restarts. Qdrant gives the project a realistic production-style retrieval layer instead of relying on in-memory development search.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ul><li>Policy and SEC chunks are embedded with provider embeddings.</li><li>The Qdrant collection is created based on the first embedding dimension.</li><li>Query embeddings search the collection.</li><li>Payload metadata stores title, source type, citation, URL, section, and chunk text.</li></ul><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Provider embeddings improve retrieval quality but require configuration.</li><li>Collection dimension validation prevents silent model mismatch.</li><li>In-memory fallback remains useful for tests but is not the primary production path.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>Embedding model is missing.</li><li>Provider does not support embeddings.</li><li>Existing Qdrant collection has a different vector dimension.</li><li>Bad chunking causes relevant evidence to rank poorly.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>Qdrant is used because the platform needs durable vector search with metadata payloads and predictable retrieval behavior.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/qdrant-vector-retrieval.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const qdrantVectorRetrieval = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  qdrantVectorRetrieval as default
};
