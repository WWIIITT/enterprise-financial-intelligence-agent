import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Environment Variables","description":"","frontmatter":{},"headers":[],"relativePath":"reference/environment-variables.md","filePath":"reference/environment-variables.md","lastUpdated":null}');
const _sfc_main = { name: "reference/environment-variables.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="environment-variables" tabindex="-1">Environment Variables <a class="header-anchor" href="#environment-variables" aria-label="Permalink to &quot;Environment Variables&quot;">​</a></h1><table tabindex="0"><thead><tr><th>Variable</th><th>Purpose</th></tr></thead><tbody><tr><td><code>LLM_API_KEY</code></td><td>API key for the OpenAI-compatible chat provider</td></tr><tr><td><code>LLM_BASE_URL</code></td><td>Chat provider base URL, usually ending in <code>/v1</code></td></tr><tr><td><code>LLM_MODEL</code></td><td>Chat model identifier</td></tr><tr><td><code>EMBEDDING_API_KEY</code></td><td>Optional separate key for embedding provider</td></tr><tr><td><code>EMBEDDING_BASE_URL</code></td><td>Optional separate embedding provider base URL</td></tr><tr><td><code>EMBEDDING_MODEL</code></td><td>Text embedding model used for Qdrant vectors</td></tr><tr><td><code>DATABASE_URL</code></td><td>PostgreSQL connection string</td></tr><tr><td><code>QDRANT_URL</code></td><td>Qdrant vector database URL</td></tr><tr><td><code>REDIS_URL</code></td><td>Redis connection string</td></tr><tr><td><code>FRED_API_KEY</code></td><td>Optional key for live FRED macro data</td></tr><tr><td><code>SEC_USER_AGENT</code></td><td>Required identifiable user agent for live SEC requests</td></tr></tbody></table><h2 id="notes" tabindex="-1">Notes <a class="header-anchor" href="#notes" aria-label="Permalink to &quot;Notes&quot;">​</a></h2><ul><li>Do not commit <code>.env</code></li><li>Qdrant requires a text embedding model, not a reranker</li><li>FRED has sample fallback for local demo</li><li>SEC live ingestion should always use a real user agent</li></ul></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("reference/environment-variables.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const environmentVariables = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  environmentVariables as default
};
