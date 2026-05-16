import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"External Sources","description":"","frontmatter":{},"headers":[],"relativePath":"reference/external-sources.md","filePath":"reference/external-sources.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "reference/external-sources.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="external-sources" tabindex="-1">External Sources <a class="header-anchor" href="#external-sources" aria-label="Permalink to &quot;External Sources&quot;">​</a></h1><p>This project uses public data sources and public documentation. The website links to sources rather than copying their content.</p><h2 id="data-sources" tabindex="-1">Data Sources <a class="header-anchor" href="#data-sources" aria-label="Permalink to &quot;Data Sources&quot;">​</a></h2><ul><li>SEC EDGAR APIs: <a href="https://www.sec.gov/search-filings/edgar-application-programming-interfaces" target="_blank" rel="noreferrer">https://www.sec.gov/search-filings/edgar-application-programming-interfaces</a></li><li>SEC Company Facts API: <a href="https://data.sec.gov/api/xbrl/companyfacts/" target="_blank" rel="noreferrer">https://data.sec.gov/api/xbrl/companyfacts/</a></li><li>FRED API: <a href="https://fred.stlouisfed.org/docs/api/fred/" target="_blank" rel="noreferrer">https://fred.stlouisfed.org/docs/api/fred/</a></li></ul><h2 id="framework-and-tooling-references" tabindex="-1">Framework And Tooling References <a class="header-anchor" href="#framework-and-tooling-references" aria-label="Permalink to &quot;Framework And Tooling References&quot;">​</a></h2><ul><li>VitePress: <a href="https://vitepress.dev/" target="_blank" rel="noreferrer">https://vitepress.dev/</a></li><li>VitePress Deploy Guide: <a href="https://vitepress.dev/guide/deploy" target="_blank" rel="noreferrer">https://vitepress.dev/guide/deploy</a></li><li>FastAPI: <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer">https://fastapi.tiangolo.com/</a></li><li>LangGraph: <a href="https://langchain-ai.github.io/langgraph/" target="_blank" rel="noreferrer">https://langchain-ai.github.io/langgraph/</a></li><li>Qdrant: <a href="https://qdrant.tech/documentation/" target="_blank" rel="noreferrer">https://qdrant.tech/documentation/</a></li><li>SQLAlchemy: <a href="https://docs.sqlalchemy.org/" target="_blank" rel="noreferrer">https://docs.sqlalchemy.org/</a></li></ul><h2 id="layout-inspiration" tabindex="-1">Layout Inspiration <a class="header-anchor" href="#layout-inspiration" aria-label="Permalink to &quot;Layout Inspiration&quot;">​</a></h2><ul><li>Hello-Agents: <a href="https://hello-agents.datawhale.cc/" target="_blank" rel="noreferrer">https://hello-agents.datawhale.cc/</a></li></ul><p>The site adopts a similar learning-document structure: left navigation, long-form chapter pages, and anchor-based reading. It does not copy the Hello-Agents content or include a discussion forum.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("reference/external-sources.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const externalSources = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  externalSources as default
};
