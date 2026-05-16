import React, { FormEvent, useEffect, useState } from "react";
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

type ConfigStatus = {
  service: string;
  llm_provider_configured: boolean;
  embedding_configured: boolean;
  database_configured: boolean;
  qdrant_configured: boolean;
  redis_configured: boolean;
  fred_configured: boolean;
  sec_user_agent_configured: boolean;
};

const dataSources = ["SEC EDGAR", "FRED", "Internal Policies", "PostgreSQL", "Qdrant"];

const defaultQuestion = "What does the AI Usage Policy say about approved use?";

function App() {
  const [question, setQuestion] = useState(defaultQuestion);
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [ingestResults, setIngestResults] = useState<IngestResponse[]>([]);
  const [error, setError] = useState("");
  const [configStatus, setConfigStatus] = useState<ConfigStatus | null>(null);
  const [configError, setConfigError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [ingesting, setIngesting] = useState<"policy" | "sec" | null>(null);
  const [isConfigLoading, setIsConfigLoading] = useState(false);
  const [secTicker, setSecTicker] = useState("AAPL");
  const [secFormType, setSecFormType] = useState("10-K");
  const [secFilingYear, setSecFilingYear] = useState("");
  const [secAccessionNumber, setSecAccessionNumber] = useState("");

  useEffect(() => {
    void loadConfigStatus();
  }, []);

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

  async function ingestLiveSecFiling() {
    const payload: Record<string, string | number> = {
      source: "edgar",
      ticker: secTicker.trim() || "AAPL",
      form_type: secFormType
    };
    const year = Number(secFilingYear);
    if (secFilingYear.trim() && Number.isInteger(year)) {
      payload.filing_year = year;
    }
    if (secAccessionNumber.trim()) {
      payload.accession_number = secAccessionNumber.trim();
    }
    await runIngestion("sec", "/api/ingest/sec", payload);
    setQuestion(`What risks are mentioned for ${payload.ticker}?`);
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

  async function loadConfigStatus() {
    setIsConfigLoading(true);
    setConfigError("");

    try {
      const apiResponse = await fetch("/api/config/status");
      if (!apiResponse.ok) {
        throw new Error(`Config check failed with status ${apiResponse.status}`);
      }

      const body = (await apiResponse.json()) as ConfigStatus;
      setConfigStatus(body);
    } catch (caughtError) {
      setConfigStatus(null);
      setConfigError(caughtError instanceof Error ? caughtError.message : "Unable to load config status.");
    } finally {
      setIsConfigLoading(false);
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
          <a href="#status">System Status</a>
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
                <FormattedAnswer answer={response.answer} />
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
            <div className="sec-ingest-controls">
              <label>
                <span>Ticker</span>
                <input value={secTicker} onChange={(event) => setSecTicker(event.target.value.toUpperCase())} />
              </label>
              <label>
                <span>Form</span>
                <select value={secFormType} onChange={(event) => setSecFormType(event.target.value)}>
                  <option value="10-K">10-K</option>
                  <option value="10-Q">10-Q</option>
                </select>
              </label>
              <label>
                <span>Year</span>
                <input
                  inputMode="numeric"
                  placeholder="optional"
                  value={secFilingYear}
                  onChange={(event) => setSecFilingYear(event.target.value)}
                />
              </label>
              <label className="wide-field">
                <span>Accession</span>
                <input
                  placeholder="optional"
                  value={secAccessionNumber}
                  onChange={(event) => setSecAccessionNumber(event.target.value)}
                />
              </label>
              <button className="secondary-button wide-field" type="button" onClick={ingestLiveSecFiling} disabled={ingesting !== null}>
                {ingesting === "sec" ? <Loader2 className="spin" size={18} /> : <PlayCircle size={18} />}
                Ingest Live SEC Filing
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

          <article id="status" className="panel">
            <div className="panel-title">
              <ShieldCheck size={20} />
              <h3>System Status</h3>
            </div>
            <button className="secondary-button status-refresh" type="button" onClick={loadConfigStatus} disabled={isConfigLoading}>
              {isConfigLoading ? <Loader2 className="spin" size={18} /> : null}
              Refresh Status
            </button>
            {configError ? <p className="error-text">{configError}</p> : null}
            <div className="status-list">
              {configStatus ? (
                <>
                  <StatusRow label="LLM Provider" ready={configStatus.llm_provider_configured} />
                  <StatusRow label="Embedding Model" ready={configStatus.embedding_configured} />
                  <StatusRow label="PostgreSQL" ready={configStatus.database_configured} />
                  <StatusRow label="Qdrant" ready={configStatus.qdrant_configured} />
                  <StatusRow label="Redis" ready={configStatus.redis_configured} />
                  <StatusRow label="SEC User Agent" ready={configStatus.sec_user_agent_configured} />
                  <StatusRow label="FRED API" ready={configStatus.fred_configured} optional />
                </>
              ) : (
                <p className="body-copy">Waiting for backend config status.</p>
              )}
            </div>
          </article>
        </section>
      </section>
    </main>
  );
}

function FormattedAnswer({ answer }: { answer: string }) {
  const blocks = parseAnswerBlocks(answer);

  return (
    <div className="formatted-answer">
      {blocks.map((block, index) => {
        if (block.type === "heading") {
          return <h4 key={`${block.content}-${index}`}>{block.content}</h4>;
        }
        if (block.type === "list") {
          return (
            <ul key={`${block.items.join("-")}-${index}`}>
              {block.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          );
        }
        return <p key={`${block.content}-${index}`}>{block.content}</p>;
      })}
    </div>
  );
}

type AnswerBlock =
  | { type: "heading"; content: string }
  | { type: "paragraph"; content: string }
  | { type: "list"; items: string[] };

function parseAnswerBlocks(answer: string): AnswerBlock[] {
  const lines = answer.split(/\r?\n/);
  const blocks: AnswerBlock[] = [];
  let paragraphLines: string[] = [];
  let listItems: string[] = [];

  function flushParagraph() {
    if (paragraphLines.length) {
      blocks.push({ type: "paragraph", content: paragraphLines.join(" ").trim() });
      paragraphLines = [];
    }
  }

  function flushList() {
    if (listItems.length) {
      blocks.push({ type: "list", items: listItems });
      listItems = [];
    }
  }

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      flushParagraph();
      flushList();
      continue;
    }

    if (line.startsWith("## ")) {
      flushParagraph();
      flushList();
      blocks.push({ type: "heading", content: line.replace(/^##\s+/, "") });
      continue;
    }

    if (line.startsWith("- ")) {
      flushParagraph();
      listItems.push(line.replace(/^-\s+/, ""));
      continue;
    }

    flushList();
    paragraphLines.push(line);
  }

  flushParagraph();
  flushList();

  return blocks.length ? blocks : [{ type: "paragraph", content: answer }];
}

function StatusRow({ label, ready, optional = false }: { label: string; ready: boolean; optional?: boolean }) {
  return (
    <div className="status-row">
      <span>{label}</span>
      <strong className={ready ? "ready" : optional ? "optional" : "missing"}>
        {ready ? "Ready" : optional ? "Later" : "Missing"}
      </strong>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
