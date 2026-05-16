import { ssrRenderAttrs, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Chat Request Lifecycle","description":"","frontmatter":{},"headers":[],"relativePath":"workflows/chat-request-lifecycle.md","filePath":"workflows/chat-request-lifecycle.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "workflows/chat-request-lifecycle.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="chat-request-lifecycle" tabindex="-1">Chat Request Lifecycle <a class="header-anchor" href="#chat-request-lifecycle" aria-label="Permalink to &quot;Chat Request Lifecycle&quot;">​</a></h1><h2 id="purpose" tabindex="-1">Purpose <a class="header-anchor" href="#purpose" aria-label="Permalink to &quot;Purpose&quot;">​</a></h2><p>This workflow explains what happens when a user sends a message to <code>/api/chat</code>.</p><h2 id="flow" tabindex="-1">Flow <a class="header-anchor" href="#flow" aria-label="Permalink to &quot;Flow&quot;">​</a></h2><div class="language-mermaid vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">mermaid</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">sequenceDiagram</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    participant User</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    participant API as FastAPI</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    participant Security as Security Preflight</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    participant Graph as LangGraph Orchestrator</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    participant Agent as Selected Agent</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    participant Logs as Request Logs</span></span>
<span class="line"></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    User-&gt;&gt;API: POST /api/chat</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    API-&gt;&gt;Security: check message</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    alt blocked</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        Security--&gt;&gt;API: block</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        API--&gt;&gt;User: governance response</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    else allow or mask</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        Security--&gt;&gt;Graph: safe message</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        Graph-&gt;&gt;Graph: route decision</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        Graph-&gt;&gt;Agent: execute route</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        Agent--&gt;&gt;Graph: answer, sources, trace, metrics</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        Graph--&gt;&gt;API: ChatResponse</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        API-&gt;&gt;Logs: write request log</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">        API--&gt;&gt;User: answer + sources + trace</span></span>
<span class="line"><span style="${ssrRenderStyle({ "--shiki-light": "#24292E", "--shiki-dark": "#E1E4E8" })}">    end</span></span></code></pre></div><h2 id="key-decisions" tabindex="-1">Key Decisions <a class="header-anchor" href="#key-decisions" aria-label="Permalink to &quot;Key Decisions&quot;">​</a></h2><ul><li>Security runs before retrieval or tool access.</li><li>The frontend response shape stays stable.</li><li>The trace exposes route decisions and agent execution.</li></ul><h2 id="what-to-watch-in-a-demo" tabindex="-1">What To Watch In A Demo <a class="header-anchor" href="#what-to-watch-in-a-demo" aria-label="Permalink to &quot;What To Watch In A Demo&quot;">​</a></h2><p>Use the Agent Trace panel to show <code>security_preflight</code>, <code>route</code>, selected agent step, and <code>respond</code>.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("workflows/chat-request-lifecycle.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const chatRequestLifecycle = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  chatRequestLifecycle as default
};
