import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"SQL Analytics Flow","description":"","frontmatter":{},"headers":[],"relativePath":"workflows/sql-analytics-flow.md","filePath":"workflows/sql-analytics-flow.md","lastUpdated":null}');
const _sfc_main = { name: "workflows/sql-analytics-flow.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="sql-analytics-flow" tabindex="-1">SQL Analytics Flow <a class="header-anchor" href="#sql-analytics-flow" aria-label="Permalink to &quot;SQL Analytics Flow&quot;">​</a></h1><h2 id="purpose" tabindex="-1">Purpose <a class="header-anchor" href="#purpose" aria-label="Permalink to &quot;Purpose&quot;">​</a></h2><p>This workflow explains how structured financial facts are ingested and queried safely.</p><h2 id="flow" tabindex="-1">Flow <a class="header-anchor" href="#flow" aria-label="Permalink to &quot;Flow&quot;">​</a></h2><div class="language-mermaid vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">mermaid</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">flowchart TD</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Ingest[Ingest Company Facts] --&gt; SEC[SEC Company Facts API or Sample]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    SEC --&gt; Normalize[Normalize Concepts]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Normalize --&gt; Facts[(PostgreSQL Financial Facts)]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Analyze[SQL Analyze Request] --&gt; Validate[Validate Metric]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Validate --&gt; Template[Safe Query Template]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Template --&gt; Facts</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Facts --&gt; Response[Trend Summary + Sources]</span></span></code></pre></div><h2 id="safety-rule" tabindex="-1">Safety Rule <a class="header-anchor" href="#safety-rule" aria-label="Permalink to &quot;Safety Rule&quot;">​</a></h2><p>The system does not accept raw SQL and does not ask an LLM to generate SQL. It only supports predefined metrics and query templates.</p><h2 id="what-to-watch-in-a-demo" tabindex="-1">What To Watch In A Demo <a class="header-anchor" href="#what-to-watch-in-a-demo" aria-label="Permalink to &quot;What To Watch In A Demo&quot;">​</a></h2><p>Run company facts ingestion for AAPL, then analyze annual revenue. The response should cite SEC Company Facts.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("workflows/sql-analytics-flow.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const sqlAnalyticsFlow = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  sqlAnalyticsFlow as default
};
