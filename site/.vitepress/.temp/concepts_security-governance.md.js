import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"Security Governance","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/security-governance.md","filePath":"concepts/security-governance.md","lastUpdated":null}');
const _sfc_main = { name: "concepts/security-governance.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="security-governance" tabindex="-1">Security Governance <a class="header-anchor" href="#security-governance" aria-label="Permalink to &quot;Security Governance&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>Security governance is the set of controls that detect sensitive input, block prompt injection, mask PII, and create audit records without storing raw sensitive text.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>Financial enterprise systems must protect client data, confidential information, and policy boundaries before any agent or tool executes.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ul><li><code>/api/security/check</code> runs standalone guardrail checks.</li><li><code>/api/chat</code> runs security preflight before LangGraph routing.</li><li>Medium-risk PII is masked.</li><li>High-risk prompt injection is blocked.</li><li>Security audit records store message hash, risk level, action, finding count, and agent.</li></ul><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Rule-based checks are transparent and fast.</li><li>They do not replace complete enterprise DLP or access control.</li><li>The MVP avoids storing raw sensitive text.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>Sophisticated prompt injection may bypass patterns.</li><li>False positives can block legitimate requests.</li><li>Future RBAC and SSO are still needed.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>The project puts security before retrieval and tool use. That ordering matters because unsafe input should not reach downstream agents.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/security-governance.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const securityGovernance = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  securityGovernance as default
};
