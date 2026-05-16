import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Macro Analysis Flow","description":"","frontmatter":{},"headers":[],"relativePath":"workflows/macro-analysis-flow.md","filePath":"workflows/macro-analysis-flow.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "workflows/macro-analysis-flow.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="macro-analysis-flow" tabindex="-1">Macro Analysis Flow <a class="header-anchor" href="#macro-analysis-flow" aria-label="Permalink to &quot;Macro Analysis Flow&quot;">​</a></h1><h2 id="purpose" tabindex="-1">Purpose <a class="header-anchor" href="#purpose" aria-label="Permalink to &quot;Purpose&quot;">​</a></h2><p>This workflow explains how the Macro Analysis Agent loads and summarizes FRED macroeconomic series.</p><h2 id="flow" tabindex="-1">Flow <a class="header-anchor" href="#flow" aria-label="Permalink to &quot;Flow&quot;">​</a></h2><div class="language-mermaid vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">mermaid</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">flowchart TD</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Request[Macro Analyze Request] --&gt; Series[Resolve Series IDs]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Series --&gt; Cache[(PostgreSQL Macro Cache)]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Cache --&gt;|cache miss| Fred[FRED API]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Fred --&gt; Cache</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Cache --&gt; Summary[Trend Summary]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Summary --&gt; Sources[FRED Citations]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Sources --&gt; Response[Macro Analyze Response]</span></span></code></pre></div><h2 id="supported-series" tabindex="-1">Supported Series <a class="header-anchor" href="#supported-series" aria-label="Permalink to &quot;Supported Series&quot;">​</a></h2><ul><li><code>FEDFUNDS</code>: Federal Funds Effective Rate</li><li><code>CPIAUCSL</code>: Consumer Price Index</li><li><code>UNRATE</code>: Unemployment Rate</li><li><code>GDP</code>: Gross Domestic Product</li><li><code>DGS10</code>: 10-Year Treasury Constant Maturity Rate</li></ul><h2 id="what-to-watch-in-a-demo" tabindex="-1">What To Watch In A Demo <a class="header-anchor" href="#what-to-watch-in-a-demo" aria-label="Permalink to &quot;What To Watch In A Demo&quot;">​</a></h2><p>Ask: <code>How do interest rates affect Apple valuation risk?</code> The system can combine macro context with document evidence when company data exists.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("workflows/macro-analysis-flow.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const macroAnalysisFlow = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  macroAnalysisFlow as default
};
