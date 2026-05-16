import { ssrRenderAttrs } from "vue/server-renderer";
import { useSSRContext } from "vue";
import { _ as _export_sfc } from "./plugin-vue_export-helper.1tPrXgE0.js";
const __pageData = JSON.parse('{"title":"SEC EDGAR Ingestion","description":"","frontmatter":{},"headers":[],"relativePath":"concepts/sec-edgar-ingestion.md","filePath":"concepts/sec-edgar-ingestion.md","lastUpdated":1778952706000}');
const _sfc_main = { name: "concepts/sec-edgar-ingestion.md" };
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)}><h1 id="sec-edgar-ingestion" tabindex="-1">SEC EDGAR Ingestion <a class="header-anchor" href="#sec-edgar-ingestion" aria-label="Permalink to &quot;SEC EDGAR Ingestion&quot;">​</a></h1><h2 id="definition" tabindex="-1">Definition <a class="header-anchor" href="#definition" aria-label="Permalink to &quot;Definition&quot;">​</a></h2><p>SEC EDGAR ingestion downloads company filings such as 10-K and 10-Q reports, cleans the filing text, parses sections, chunks the content, embeds the chunks, and indexes them for document research.</p><h2 id="why-it-exists-in-aurelia-ledger" tabindex="-1">Why It Exists In Aurelia Ledger <a class="header-anchor" href="#why-it-exists-in-aurelia-ledger" aria-label="Permalink to &quot;Why It Exists In Aurelia Ledger&quot;">​</a></h2><p>SEC filings are primary-source evidence for company risk, business strategy, financial disclosures, and management discussion.</p><h2 id="how-it-works-in-this-repo" tabindex="-1">How It Works In This Repo <a class="header-anchor" href="#how-it-works-in-this-repo" aria-label="Permalink to &quot;How It Works In This Repo&quot;">​</a></h2><ul><li>Ticker is resolved to CIK.</li><li>Filing selection supports latest form, filing year, or accession number.</li><li>SEC requests use a configured <code>SEC_USER_AGENT</code>.</li><li>HTML is cleaned and common encoding issues are repaired.</li><li>Section parser assigns labels such as Business, Risk Factors, MD&amp;A, and Market Risk.</li><li>Chunks are indexed with SEC citation metadata.</li></ul><h2 id="design-tradeoffs" tabindex="-1">Design Tradeoffs <a class="header-anchor" href="#design-tradeoffs" aria-label="Permalink to &quot;Design Tradeoffs&quot;">​</a></h2><ul><li>Deterministic parsing is transparent and testable.</li><li>SEC throttling and retry behavior reduce external API fragility.</li><li>The parser is not a full XBRL or filing structure engine.</li></ul><h2 id="failure-modes" tabindex="-1">Failure Modes <a class="header-anchor" href="#failure-modes" aria-label="Permalink to &quot;Failure Modes&quot;">​</a></h2><ul><li>Missing SEC user agent.</li><li>Ticker or filing not found.</li><li>SEC rate limiting.</li><li>Filing text is too noisy or section headings are unusual.</li></ul><h2 id="interview-explanation" tabindex="-1">Interview Explanation <a class="header-anchor" href="#interview-explanation" aria-label="Permalink to &quot;Interview Explanation&quot;">​</a></h2><p>The SEC connector shows the system can ingest real regulatory documents, not just curated local samples.</p></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("concepts/sec-edgar-ingestion.md");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const secEdgarIngestion = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);
export {
  __pageData,
  secEdgarIngestion as default
};
