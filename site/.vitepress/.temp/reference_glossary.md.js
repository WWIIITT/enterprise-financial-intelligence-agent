import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Glossary","description":"","frontmatter":{},"headers":[],"relativePath":"reference/glossary.md","filePath":"reference/glossary.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "reference/glossary.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="glossary" tabindex="-1">Glossary <a class="header-anchor" href="#glossary" aria-label="Permalink to &quot;Glossary&quot;">​</a></h1><table tabindex="0"><thead><tr><th>Term</th><th>Meaning</th></tr></thead><tbody><tr><td>RAG</td><td>Retrieval-Augmented Generation</td></tr><tr><td>Qdrant</td><td>Vector database used for semantic retrieval</td></tr><tr><td>SEC EDGAR</td><td>Public SEC filing system</td></tr><tr><td>FRED</td><td>Federal Reserve Economic Data</td></tr><tr><td>Company Facts</td><td>SEC XBRL structured company data</td></tr><tr><td>LangGraph</td><td>Workflow framework used for agent routing</td></tr><tr><td>Guardrail</td><td>Preflight rule that masks, blocks, or allows a request</td></tr><tr><td>Evaluation suite</td><td>Group of deterministic test cases</td></tr><tr><td>Citation score</td><td>Evaluation measure for required citation terms</td></tr><tr><td>Source coverage</td><td>Evaluation measure for expected source availability</td></tr><tr><td>P95 latency</td><td>95th percentile latency</td></tr></tbody></table></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("reference/glossary.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const glossary = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  glossary as default
};
