import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Deployment","description":"","frontmatter":{},"headers":[],"relativePath":"reference/deployment.md","filePath":"reference/deployment.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "reference/deployment.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="deployment" tabindex="-1">Deployment <a class="header-anchor" href="#deployment" aria-label="Permalink to &quot;Deployment&quot;">​</a></h1><h2 id="knowledge-site" tabindex="-1">Knowledge Site <a class="header-anchor" href="#knowledge-site" aria-label="Permalink to &quot;Knowledge Site&quot;">​</a></h2><p>The knowledge site is designed for GitHub Pages.</p><ol><li>Commit and push the <code>site/</code> directory and <code>.github/workflows/deploy-knowledge-site.yml</code></li><li>In GitHub repository settings, enable Pages</li><li>Choose GitHub Actions as the build and deployment source</li><li>Push to <code>main</code> or run the workflow manually</li></ol><p>Expected public URL:</p><div class="language-text vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>https://&lt;github-user&gt;.github.io/enterprise-financial-intelligence-agent/</span></span></code></pre></div><h2 id="dashboard-and-api" tabindex="-1">Dashboard And API <a class="header-anchor" href="#dashboard-and-api" aria-label="Permalink to &quot;Dashboard And API&quot;">​</a></h2><p>The current dashboard and backend remain local or deployable separately. The knowledge site is static and does not require the backend.</p><h2 id="production-path" tabindex="-1">Production Path <a class="header-anchor" href="#production-path" aria-label="Permalink to &quot;Production Path&quot;">​</a></h2><p>For production, deploy the backend, frontend dashboard, PostgreSQL, Qdrant, and Redis through a managed cloud or container platform. See <code>docs/deployment-roadmap.md</code> for the staged deployment plan.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("reference/deployment.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const deployment = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  deployment as default
};
