import React from "react";
import ReactDOM from "react-dom/client";
import { Activity, Database, FileSearch, GitBranch, ShieldCheck } from "lucide-react";
import "./styles.css";

const traceSteps = [
  "Receive user question",
  "Route through orchestrator",
  "Select document, macro, policy, or SQL agent",
  "Return cited answer with metrics"
];

const dataSources = ["SEC EDGAR", "FRED", "Internal Policies", "PostgreSQL", "Qdrant"];

function App() {
  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Enterprise Financial Intelligence</p>
          <h1>Aurelia Ledger</h1>
        </div>
        <nav className="nav-list" aria-label="Main sections">
          <a href="#chat">Chat Console</a>
          <a href="#trace">Agent Trace</a>
          <a href="#sources">Data Sources</a>
          <a href="#evals">Evaluation</a>
        </nav>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Phase 1 Skeleton</p>
            <h2>AI research, compliance, and macro intelligence workspace</h2>
          </div>
          <span className="status-pill">API-ready placeholder</span>
        </header>

        <section className="grid">
          <article id="chat" className="panel panel-large">
            <div className="panel-title">
              <FileSearch size={20} />
              <h3>Chat Console</h3>
            </div>
            <textarea
              aria-label="Question"
              placeholder="Ask about a company filing, macro trend, internal policy, or SQL metric..."
            />
            <button type="button">Run Agent Workflow</button>
          </article>

          <article id="trace" className="panel">
            <div className="panel-title">
              <GitBranch size={20} />
              <h3>Agent Trace</h3>
            </div>
            <ol className="trace-list">
              {traceSteps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>
          </article>

          <article id="sources" className="panel">
            <div className="panel-title">
              <Database size={20} />
              <h3>Data Sources</h3>
            </div>
            <div className="source-list">
              {dataSources.map((source) => (
                <span key={source}>{source}</span>
              ))}
            </div>
          </article>

          <article id="evals" className="panel">
            <div className="panel-title">
              <Activity size={20} />
              <h3>Evaluation / Monitoring</h3>
            </div>
            <dl className="metric-list">
              <div><dt>Latency</dt><dd>placeholder</dd></div>
              <div><dt>Token Cost</dt><dd>placeholder</dd></div>
              <div><dt>Faithfulness</dt><dd>placeholder</dd></div>
            </dl>
          </article>

          <article className="panel">
            <div className="panel-title">
              <ShieldCheck size={20} />
              <h3>Governance</h3>
            </div>
            <p className="body-copy">
              Policy RAG, PII masking, prompt-injection checks, audit logs, and architecture documentation are planned for the next phases.
            </p>
          </article>
        </section>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
