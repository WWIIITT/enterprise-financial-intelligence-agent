import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Security Preflight Flow","description":"","frontmatter":{},"headers":[],"relativePath":"workflows/security-preflight-flow.md","filePath":"workflows/security-preflight-flow.md","lastUpdated":null}');
const _sfc_main = { name: "workflows/security-preflight-flow.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="security-preflight-flow" tabindex="-1">Security Preflight Flow <a class="header-anchor" href="#security-preflight-flow" aria-label="Permalink to &quot;Security Preflight Flow&quot;">​</a></h1><h2 id="purpose" tabindex="-1">Purpose <a class="header-anchor" href="#purpose" aria-label="Permalink to &quot;Purpose&quot;">​</a></h2><p>This workflow explains how the system handles sensitive or malicious input before agent routing.</p><h2 id="flow" tabindex="-1">Flow <a class="header-anchor" href="#flow" aria-label="Permalink to &quot;Flow&quot;">​</a></h2><div class="language-mermaid vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">mermaid</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">flowchart TD</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Message[User Message] --&gt; Detect[PII and Injection Detection]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Detect --&gt; Risk[Risk Level]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Risk --&gt;|low| Allow[Allow]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Risk --&gt;|medium| Mask[Mask Sensitive Values]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Risk --&gt;|high| Block[Block Request]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Allow --&gt; Audit[(Audit Hash)]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Mask --&gt; Audit</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Block --&gt; Audit</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Mask --&gt; Orchestrator[Continue With Masked Message]</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Allow --&gt; Orchestrator</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    Block --&gt; Response[Governance Response]</span></span></code></pre></div><h2 id="current-controls" tabindex="-1">Current Controls <a class="header-anchor" href="#current-controls" aria-label="Permalink to &quot;Current Controls&quot;">​</a></h2><ul><li>Email, phone, SSN, card-like, and secret-like token detection</li><li>Prompt injection and policy bypass pattern detection</li><li>Message hash audit records</li></ul><h2 id="what-to-watch-in-a-demo" tabindex="-1">What To Watch In A Demo <a class="header-anchor" href="#what-to-watch-in-a-demo" aria-label="Permalink to &quot;What To Watch In A Demo&quot;">​</a></h2><p>Run a standalone security check with an email address, then run a prompt injection message through <code>/api/chat</code>.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("workflows/security-preflight-flow.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const securityPreflightFlow = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  securityPreflightFlow as default
};
