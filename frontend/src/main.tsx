import React, { FormEvent, useState } from "react";
import ReactDOM from "react-dom/client";
import { Activity, Database, FileSearch, GitBranch, Loader2, PlayCircle, ShieldCheck } from "lucide-react";
import "./styles.css";

type Source = {
  title: string;
  url: string | null;
  citation: string | null;
  source_type: string | null;
};

type TraceStep = {
  step: string;
  detail: string;
};

type Metrics = {
  latency_ms: number;
  estimated_cost_usd: number;
  tokens_input: number;
  tokens_output: number;
};

type ChatResponse = {
  answer: string;
  agent: string;
  sources: Source[];
  trace: TraceStep[];
  metrics: Metrics;
};

type IngestResponse = {
  status: string;
  source_type: string;
  source: string;
  documents_indexed: number;
  chunks_indexed: number;
  vector_backend: string;
  message: string;
};

const dataSources = ["SEC EDGAR", "FRED", "Internal Policies", "PostgreSQL", "Qdrant"];

const defaultQuestion = "What does the AI Usage Policy say about approved use?";

function App() {
  const [question, setQuestion] = useState(defaultQuestion);
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [ingestResults, setIngestResults] = useState<IngestResponse[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [ingesting, setIngesting] = useState<"policy" | "sec" | null>(null);

  async function submitQuestion(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion) {
      setError("Enter a question before running the workflow.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const apiResponse = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmedQuestion })
      });

      if (!apiResponse.ok) {
        throw new Error(`API request failed with status ${apiResponse.status}`);
      }

      const body = (await apiResponse.json()) as ChatResponse;
      setResponse(body);
    } catch (caughtError) {
      setResponse(null);
      setError(caughtError instanceof Error ? caughtError.message : "Unable to reach the API.");
    } finally {
      setIsLoading(false);
    }
  }

  async function ingestPolicyDocs() {
    await runIngestion("policy", "/api/ingest/policy", { source: "all" });
  }

  async function ingestSecSample() {
    await runIngestion("sec", "/api/ingest/sec", {
      source: "sample-sec-inline",
      ticker: "AAPL",
      content:
        "Apple reports revenue risk from foreign exchange, interest rates, product demand, supply chain constraints, and macroeconomic uncertainty."
    });
    setQuestion("What risks are mentioned for Apple?");
  }

  async function runIngestion(kind: "policy" | "sec", endpoint: string, payload: object) {
    setIngesting(kind);
    setError("");

    try {
      const apiResponse = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!apiResponse.ok) {
        throw new Error(`Ingestion failed with status ${apiResponse.status}`);
      }

      const body = (await apiResponse.json()) as IngestResponse;
      setIngestResults((currentResults) => [body, ...currentResults.filter((item) => item.source_type !== body.source_type)]);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Unable to run ingestion.");
    } finally {
      setIngesting(null);
    }
  }

  const traceSteps = response?.trace ?? [
    { step: "receive", detail: "Waiting for a user question." },
    { step: "route", detail: "The backend will retrieve indexed policy or SEC evidence." },
    { step: "respond", detail: "The answer, sources, and metrics will appear after submission." }
  ];

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
            <p className="eyebrow">Phase 1 RAG MVP</p>
            <h2>AI research, compliance, and macro intelligence workspace</h2>
          </div>
          <span className="status-pill">{response ? response.agent : "API-connected console"}</span>
        </header>

        <section className="grid">
          <article id="chat" className="panel panel-large">
            <div className="panel-title">
              <FileSearch size={20} />
              <h3>Chat Console</h3>
            </div>
            <form onSubmit={submitQuestion}>
              <textarea
                aria-label="Question"
                placeholder="Ask about a company filing, macro trend, internal policy, or SQL metric..."
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
              />
              <div className="button-row">
                <button type="submit" disabled={isLoading}>
                  {isLoading ? <Loader2 className="spin" size={18} /> : null}
                  {isLoading ? "Running Workflow" : "Run Agent Workflow"}
                </button>
                <button
                  className="secondary-button"
                  type="button"
                  onClick={() => setQuestion("What risks are mentioned for Apple?")}
                >
                  Apple Risk
                </button>
              </div>
            </form>
            {error ? <p className="error-text">{error}</p> : null}
            {response ? (
              <section className="answer-block" aria-live="polite">
                <p className="eyebrow">Answer</p>
                <p>{response.answer}</p>
              </section>
            ) : null}
          </article>

          <article id="trace" className="panel">
            <div className="panel-title">
              <GitBranch size={20} />
              <h3>Agent Trace</h3>
            </div>
            <ol className="trace-list">
              {traceSteps.map((step) => (
                <li key={`${step.step}-${step.detail}`}>
                  <strong>{step.step}</strong>
                  <span>{step.detail}</span>
                </li>
              ))}
            </ol>
          </article>

          <article id="sources" className="panel">
            <div className="panel-title">
              <Database size={20} />
              <h3>Data Sources</h3>
            </div>
            <div className="button-row compact-row">
              <button className="secondary-button" type="button" onClick={ingestPolicyDocs} disabled={ingesting !== null}>
                {ingesting === "policy" ? <Loader2 className="spin" size={18} /> : <PlayCircle size={18} />}
                Ingest Policy Docs
              </button>
              <button className="secondary-button" type="button" onClick={ingestSecSample} disabled={ingesting !== null}>
                {ingesting === "sec" ? <Loader2 className="spin" size={18} /> : <PlayCircle size={18} />}
                Ingest SEC Sample
              </button>
            </div>
            {ingestResults.length ? (
              <div className="ingest-list">
                {ingestResults.map((result) => (
                  <div className="ingest-item" key={`${result.source_type}-${result.source}`}>
                    <strong>{result.source_type}</strong>
                    <span>{result.documents_indexed} docs / {result.chunks_indexed} chunks</span>
                    <small>{result.vector_backend}</small>
                  </div>
                ))}
              </div>
            ) : null}
            {response?.sources.length ? (
              <div className="citation-list">
                {response.sources.map((source, index) => (
                  <div className="citation-item" key={`${source.title}-${source.citation}-${index}`}>
                    <span>{source.source_type ?? "source"}</span>
                    <strong>{source.title}</strong>
                    <small>{source.citation}</small>
                  </div>
                ))}
              </div>
            ) : (
              <div className="source-list">
                {dataSources.map((source) => (
                  <span key={source}>{source}</span>
                ))}
              </div>
            )}
          </article>

          <article id="evals" className="panel">
            <div className="panel-title">
              <Activity size={20} />
              <h3>Evaluation / Monitoring</h3>
            </div>
            <dl className="metric-list">
              <div><dt>Latency</dt><dd>{response ? `${response.metrics.latency_ms} ms` : "waiting"}</dd></div>
              <div><dt>Token Cost</dt><dd>{response ? `$${response.metrics.estimated_cost_usd.toFixed(4)}` : "waiting"}</dd></div>
              <div><dt>Sources</dt><dd>{response ? response.sources.length : "waiting"}</dd></div>
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
