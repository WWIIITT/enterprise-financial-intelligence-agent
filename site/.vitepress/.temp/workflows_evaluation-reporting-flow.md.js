import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Evaluation Reporting Flow","description":"","frontmatter":{},"headers":[],"relativePath":"workflows/evaluation-reporting-flow.md","filePath":"workflows/evaluation-reporting-flow.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "workflows/evaluation-reporting-flow.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="evaluation-reporting-flow" tabindex="-1">Evaluation Reporting Flow <a class="header-anchor" href="#evaluation-reporting-flow" aria-label="Permalink to &quot;Evaluation Reporting Flow&quot;">​</a></h1><h2 id="purpose" tabindex="-1">Purpose <a class="header-anchor" href="#purpose" aria-label="Permalink to &quot;Purpose&quot;">​</a></h2><p>This workflow explains how evaluation suites become quality metrics and portfolio reports.</p><h2 id="flow" tabindex="-1">Flow <a class="header-anchor" href="#flow" aria-label="Permalink to &quot;Flow&quot;">​</a></h2><div class="language-mermaid vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">mermaid</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">flowchart TD</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Cases[JSON Eval Cases] --&gt; Runner[Evaluation Runner]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Runner --&gt; Execution[Chat or Endpoint Execution]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Execution --&gt; Scoring[Deterministic Scoring]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Scoring --&gt; Metrics[Summary Metrics]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Metrics --&gt; Report[Markdown / JSON Report]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Metrics --&gt; DB[(Evaluation Run Record)]</span></span></code></pre></div><h2 id="metrics" tabindex="-1">Metrics <a class="header-anchor" href="#metrics" aria-label="Permalink to &quot;Metrics&quot;">​</a></h2><ul><li>Pass rate</li><li>Route accuracy</li><li>Source coverage</li><li>Citation score</li><li>Answer term score</li><li>Average latency</li><li>P95 latency</li><li>Hallucination-risk count</li></ul><h2 id="what-to-watch-in-a-demo" tabindex="-1">What To Watch In A Demo <a class="header-anchor" href="#what-to-watch-in-a-demo" aria-label="Permalink to &quot;What To Watch In A Demo&quot;">​</a></h2><p>Generate <code>suite=&quot;all&quot;</code> and open <code>data/reports/evaluation-report.md</code>.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("workflows/evaluation-reporting-flow.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const evaluationReportingFlow = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  evaluationReportingFlow as default
};
