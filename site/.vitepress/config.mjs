import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Aurelia Ledger",
  description: "Enterprise Financial Intelligence Agent Platform learning site",
  base: "/enterprise-financial-intelligence-agent/",
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "Home", link: "/" },
      { text: "Sprints", link: "/sprints/sprint-01-rag-mvp" },
      { text: "Concepts", link: "/concepts/rag-and-citations" },
      { text: "Workflows", link: "/workflows/chat-request-lifecycle" },
      { text: "Reference", link: "/reference/api-reference" }
    ],
    sidebar: [
      {
        text: "Start Here",
        items: [
          { text: "Overview", link: "/" },
          { text: "Learning Path", link: "/reference/learning-path" }
        ]
      },
      {
        text: "Sprint Guide",
        collapsed: false,
        items: [
          { text: "Sprint 1: RAG MVP", link: "/sprints/sprint-01-rag-mvp" },
          { text: "Sprint 2: Persistent Retrieval", link: "/sprints/sprint-02-persistent-retrieval" },
          { text: "Sprint 3: SEC EDGAR", link: "/sprints/sprint-03-sec-edgar" },
          { text: "Sprint 4: Macro Agent", link: "/sprints/sprint-04-macro-agent" },
          { text: "Sprint 5: LangGraph", link: "/sprints/sprint-05-langgraph-orchestrator" },
          { text: "Sprint 6: SQL Analytics", link: "/sprints/sprint-06-sql-analytics" },
          { text: "Sprint 7: Evaluation Engine", link: "/sprints/sprint-07-evaluation-engine" },
          { text: "Sprint 8: Security", link: "/sprints/sprint-08-security-governance" },
          { text: "Sprint 9: Observability", link: "/sprints/sprint-09-observability" },
          { text: "Sprint 10: Architecture Pack", link: "/sprints/sprint-10-architecture-pack" }
        ]
      },
      {
        text: "Concept Guide",
        collapsed: false,
        items: [
          { text: "RAG and Citations", link: "/concepts/rag-and-citations" },
          { text: "Qdrant Retrieval", link: "/concepts/qdrant-vector-retrieval" },
          { text: "SEC EDGAR Ingestion", link: "/concepts/sec-edgar-ingestion" },
          { text: "FRED Macro Agent", link: "/concepts/fred-macro-agent" },
          { text: "SQL Analytics Agent", link: "/concepts/sql-analytics-agent" },
          { text: "LangGraph Orchestrator", link: "/concepts/langgraph-orchestrator" },
          { text: "Evaluation Engine", link: "/concepts/evaluation-engine" },
          { text: "Security Governance", link: "/concepts/security-governance" },
          { text: "Observability Dashboard", link: "/concepts/observability-dashboard" }
        ]
      },
      {
        text: "Workflow Guide",
        collapsed: false,
        items: [
          { text: "Chat Request Lifecycle", link: "/workflows/chat-request-lifecycle" },
          { text: "Document Ingestion", link: "/workflows/document-ingestion-flow" },
          { text: "Macro Analysis", link: "/workflows/macro-analysis-flow" },
          { text: "SQL Analytics", link: "/workflows/sql-analytics-flow" },
          { text: "Security Preflight", link: "/workflows/security-preflight-flow" },
          { text: "Evaluation Reporting", link: "/workflows/evaluation-reporting-flow" }
        ]
      },
      {
        text: "Reference",
        collapsed: false,
        items: [
          { text: "API Reference", link: "/reference/api-reference" },
          { text: "Environment Variables", link: "/reference/environment-variables" },
          { text: "Local Runbook", link: "/reference/local-runbook" },
          { text: "Deployment", link: "/reference/deployment" },
          { text: "External Sources", link: "/reference/external-sources" },
          { text: "Glossary", link: "/reference/glossary" }
        ]
      }
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/" }],
    search: { provider: "local" },
    outline: {
      level: [2, 3],
      label: "On this page"
    },
    footer: {
      message: "Built as a Senior AI Engineer and AI Solution Architect portfolio project.",
      copyright: "Aurelia Ledger"
    }
  }
});
