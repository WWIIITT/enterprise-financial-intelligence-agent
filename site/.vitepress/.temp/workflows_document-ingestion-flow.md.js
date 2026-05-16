import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Document Ingestion Flow","description":"","frontmatter":{},"headers":[],"relativePath":"workflows/document-ingestion-flow.md","filePath":"workflows/document-ingestion-flow.md","lastUpdated":null}');
const _sfc_main = { name: "workflows/document-ingestion-flow.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="document-ingestion-flow" tabindex="-1">Document Ingestion Flow <a class="header-anchor" href="#document-ingestion-flow" aria-label="Permalink to &quot;Document Ingestion Flow&quot;">​</a></h1><h2 id="purpose" tabindex="-1">Purpose <a class="header-anchor" href="#purpose" aria-label="Permalink to &quot;Purpose&quot;">​</a></h2><p>This workflow explains how policy documents and SEC filings become searchable RAG evidence.</p><h2 id="flow" tabindex="-1">Flow <a class="header-anchor" href="#flow" aria-label="Permalink to &quot;Flow&quot;">​</a></h2><div class="language-mermaid vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">mermaid</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">flowchart TD</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Source[Policy Markdown or SEC Filing] --&gt; Clean[Clean Text]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Clean --&gt; Parse[Parse Sections]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Parse --&gt; Chunk[Chunk Text]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Chunk --&gt; Embed[Embedding Provider]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Embed --&gt; Qdrant[(Qdrant)]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Chunk --&gt; Metadata[(PostgreSQL Metadata)]</span></span></code></pre></div><h2 id="policy-ingestion" tabindex="-1">Policy Ingestion <a class="header-anchor" href="#policy-ingestion" aria-label="Permalink to &quot;Policy Ingestion&quot;">​</a></h2><p>Policy documents live under <code>data/policies/</code>. They model internal AI usage, privacy, investment review, model risk, and client communication policies.</p><h2 id="sec-ingestion" tabindex="-1">SEC Ingestion <a class="header-anchor" href="#sec-ingestion" aria-label="Permalink to &quot;SEC Ingestion&quot;">​</a></h2><p>SEC filings are downloaded from EDGAR, cleaned, parsed into sections, and indexed with form type, filing date, accession number, URL, and section metadata.</p><h2 id="what-to-watch-in-a-demo" tabindex="-1">What To Watch In A Demo <a class="header-anchor" href="#what-to-watch-in-a-demo" aria-label="Permalink to &quot;What To Watch In A Demo&quot;">​</a></h2><p>Run policy ingestion, run live SEC ingestion, then ask a cited question about Apple risk or approved AI use.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("workflows/document-ingestion-flow.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const documentIngestionFlow = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  documentIngestionFlow as default
};
