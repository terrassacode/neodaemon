import { useMemo, useState } from "react";
import Papa from "papaparse";
import {
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import "./styles.css";

const TONES = {
  ciutada: "ciutadà",
  neutral: "neutralitat estricta",
  executiu: "informe executiu",
  activisme: "activisme cívic prudent",
};

const PRUDENT_TERMS = [
  "indicis de mala gestió",
  "possibles incoherències",
  "possible manca de transparència",
  "preguntes pendents",
  "possible risc institucional",
  "possible despesa difícil de justificar",
  "concentració de contractes",
  "possible desviació pressupostària",
];

function extractAmounts(text) {
  const matches =
    text.match(/(?:\d{1,3}(?:[.\s]\d{3})*|\d+)(?:,\d{2})?\s?€/g) || [];

  return matches.slice(0, 12);
}

function extractDates(text) {
  const matches =
    text.match(/\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4})\b/g) || [];

  return [...new Set(matches)].slice(0, 10);
}

function detectActors(text) {
  const matches =
    text.match(
      /\b(?:Ajuntament|Generalitat|Diputació|Consell|Empresa|Fundació|Associació|Partit|Govern|Departament)\s+[A-ZÀ-Ý][\wÀ-ÿ-]*/g
    ) || [];

  return [...new Set(matches)].slice(0, 10);
}

function parseNumericRows(csvText) {
  if (!csvText.trim()) {
    return [];
  }

  const parsed = Papa.parse(csvText, {
    header: true,
    skipEmptyLines: true,
    dynamicTyping: true,
  });

  if (parsed.errors.length || !parsed.data.length) {
    return [];
  }

  return parsed.data
    .map((row, index) => {
      const numericEntry = Object.entries(row).find(
        ([, value]) => typeof value === "number"
      );

      if (!numericEntry) {
        return null;
      }

      const labelEntry = Object.entries(row).find(
        ([, value]) => typeof value === "string"
      );

      return {
        name: labelEntry?.[1] || `Fila ${index + 1}`,
        value: numericEntry[1],
      };
    })
    .filter(Boolean)
    .slice(0, 12);
}

function buildReport({ title, inputType, url, text, csvText, tone }) {
  const allText = [title, url, text, csvText].filter(Boolean).join("\n");
  const amounts = extractAmounts(allText);
  const dates = extractDates(allText);
  const actors = detectActors(allText);
  const chartData = parseNumericRows(csvText);
  const hasEnoughData = allText.trim().length > 40 || chartData.length > 0;

  const detectedFacts = [];

  if (url) {
    detectedFacts.push(
      "S’ha indicat una URL com a referència, sense descàrrega automàtica."
    );
  }

  if (text.trim()) {
    detectedFacts.push("S’ha aportat text manual per analitzar.");
  }

  if (csvText.trim()) {
    detectedFacts.push("S’ha aportat CSV enganxat manualment.");
  }

  if (amounts.length) {
    detectedFacts.push(
      `S’han detectat ${amounts.length} possibles imports en el material aportat.`
    );
  }

  if (dates.length) {
    detectedFacts.push(`S’han detectat ${dates.length} possibles dates o anys.`);
  }

  return {
    title: title || "Cas cívic sense títol",
    tone,
    inputType,
    url,
    hasEnoughData,
    amounts,
    dates,
    actors,
    chartData,
    detectedFacts: detectedFacts.length
      ? detectedFacts
      : ["No hi ha prou elements detectables en les dades aportades."],
    interpretations: hasEnoughData
      ? [
          "El material podria requerir una revisió documental més detallada.",
          "La lectura depèn de la qualitat, l’origen i el context de les dades aportades.",
        ]
      : ["No és prudent formular interpretacions amb les dades actuals."],
    indicators: hasEnoughData
      ? [
          "possibles incoherències si hi ha imports, dates o actors sense context suficient",
          "possible manca de transparència si no consten fonts o documents justificatius",
          "possible despesa difícil de justificar si no hi ha detall pressupostari suficient",
          "possible risc institucional si les decisions no són traçables",
        ]
      : ["No hi ha indicis suficients: cal aportar més dades verificables."],
    openQuestions: hasEnoughData
      ? [
          "Quines fonts documenten els fets principals?",
          "Hi ha imports, dates i responsables clarament identificats?",
          "Existeixen alternatives o explicacions administratives no recollides?",
          "Quina part és fet verificat i quina part és interpretació?",
        ]
      : [
          "Quines dades verificables es poden aportar?",
          "Hi ha documents oficials, imports o dates concretes?",
        ],
    unverifiedData: [
      "La informació introduïda no ha estat verificada per l’eina.",
      "La URL indicada, si existeix, no s’ha descarregat ni consultat automàticament.",
      "Els actors, dates i imports detectats provenen de patrons simples i poden contenir errors.",
    ],
    executiveSummary: hasEnoughData
      ? [
          "Aquest informe és una lectura preliminar basada només en les dades aportades manualment.",
          "No afirma corrupció ni irregularitats demostrades.",
          "Separa elements detectats, interpretacions, indicis prudents, preguntes obertes i dades no verificades.",
        ]
      : [
          "No hi ha dades suficients per generar una lectura fiable.",
          "Cal aportar text, CSV o informació verificable abans d’extreure conclusions.",
        ],
  };
}

function CopyButton({ label, value }) {
  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(value);
    } catch {
      // No trenquem l'app si el navegador bloqueja el porta-retalls.
    }
  }

  return (
    <button type="button" onClick={handleCopy}>
      {label}
    </button>
  );
}

function ListSection({ title, items }) {
  return (
    <article className="panel">
      <h3>{title}</h3>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </article>
  );
}

export default function App() {
  const [inputType, setInputType] = useState("text");
  const [tone, setTone] = useState("neutral");
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");
  const [text, setText] = useState("");
  const [csvText, setCsvText] = useState("");
  const [generated, setGenerated] = useState(false);

  const report = useMemo(
    () =>
      buildReport({
        title,
        inputType,
        url,
        text,
        csvText,
        tone,
      }),
    [title, inputType, url, text, csvText, tone]
  );

  const printableSummary = [
    report.title,
    "",
    "Resum executiu:",
    ...report.executiveSummary.map((item) => `- ${item}`),
    "",
    "Fets detectats en les dades aportades:",
    ...report.detectedFacts.map((item) => `- ${item}`),
    "",
    "Preguntes obertes:",
    ...report.openQuestions.map((item) => `- ${item}`),
  ].join("\n");

  return (
    <main className="app">
      <section className="hero">
        <span className="badge">MVP local · sense APIs externes</span>
        <h1>Visualitzador Cívic CAT</h1>
        <p>
          Eina local per ordenar informació cívica amb prudència editorial:
          elements detectats, interpretacions, indicis, preguntes obertes i
          dades no verificades.
        </p>
      </section>

      <section className="panel form-panel">
        <h2>Entrada de dades</h2>

        <label>
          Títol opcional del cas
          <input
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />
        </label>

        <div className="grid two">
          <label>
            Tipus d’entrada
            <select
              value={inputType}
              onChange={(event) => setInputType(event.target.value)}
            >
              <option value="url">URL de referència</option>
              <option value="text">Text enganxat</option>
              <option value="csv">CSV</option>
              <option value="mixed">Combinat</option>
            </select>
          </label>

          <label>
            To
            <select
              value={tone}
              onChange={(event) => setTone(event.target.value)}
            >
              {Object.entries(TONES).map(([key, toneLabel]) => (
                <option key={key} value={key}>
                  {toneLabel}
                </option>
              ))}
            </select>
          </label>
        </div>

        <label>
          URL de referència, sense descàrrega automàtica
          <input
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            placeholder="https://..."
          />
        </label>

        <label>
          Text enganxat
          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            rows="7"
          />
        </label>

        <label>
          CSV enganxat
          <textarea
            value={csvText}
            onChange={(event) => setCsvText(event.target.value)}
            rows="6"
          />
        </label>

        <button
          className="primary"
          type="button"
          onClick={() => setGenerated(true)}
        >
          Generar informe
        </button>
      </section>

      {generated && (
        <section className="report">
          <div className="report-header">
            <div>
              <span className="badge">To: {TONES[tone]}</span>
              <h2>{report.title}</h2>
            </div>

            <div className="actions">
              <button type="button" onClick={() => window.print()}>
                Imprimir
              </button>
              <CopyButton
                label="Copiar resum executiu"
                value={report.executiveSummary.join("\n")}
              />
              <CopyButton
                label="Copiar preguntes pendents"
                value={report.openQuestions.join("\n")}
              />
            </div>
          </div>

          <section className="panel warning">
            <strong>Nota editorial:</strong> aquest MVP no afirma corrupció, no
            inventa dades i no substitueix verificació documental.
          </section>

          <div className="grid three kpis">
            <article>
              <strong>{report.amounts.length}</strong>
              <span>imports detectats</span>
            </article>
            <article>
              <strong>{report.dates.length}</strong>
              <span>dates detectades</span>
            </article>
            <article>
              <strong>{report.actors.length}</strong>
              <span>actors possibles</span>
            </article>
          </div>

          <ListSection title="Resum executiu" items={report.executiveSummary} />

          <section className="grid two">
            <ListSection
              title="Fets detectats en les dades aportades"
              items={report.detectedFacts}
            />
            <ListSection
              title="Interpretacions"
              items={report.interpretations}
            />
            <ListSection title="Indicis" items={report.indicators} />
            <ListSection
              title="Preguntes obertes"
              items={report.openQuestions}
            />
          </section>

          <ListSection
            title="Dades no verificades"
            items={report.unverifiedData}
          />

          <section className="grid two">
            <article className="panel">
              <h3>Actors</h3>
              {report.actors.length ? (
                <ul>
                  {report.actors.map((actor) => (
                    <li key={actor}>{actor}</li>
                  ))}
                </ul>
              ) : (
                <p>No hi ha actors suficientment detectables.</p>
              )}
            </article>

            <article className="panel">
              <h3>Línia de temps</h3>
              {report.dates.length ? (
                <ul>
                  {report.dates.map((date) => (
                    <li key={date}>{date}</li>
                  ))}
                </ul>
              ) : (
                <p>No hi ha dates suficients.</p>
              )}
            </article>
          </section>

          <section className="panel">
            <h3>Riscos / impactes prudents</h3>
            <ul>
              {report.indicators.map((indicator) => (
                <li key={indicator}>{indicator}</li>
              ))}
            </ul>
            <p className="terms">
              Llenguatge prudent: {PRUDENT_TERMS.join(" · ")}
            </p>
          </section>

          <section className="panel">
            <h3>Visualització numèrica</h3>
            {report.chartData.length >= 2 ? (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={report.chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#2563eb" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p>
                No es crea cap gràfic perquè no hi ha dades numèriques
                suficients.
              </p>
            )}
          </section>

          <section className="panel">
            <h3>Fonts</h3>
            {url ? (
              <p>{url}</p>
            ) : (
              <p>No s’ha indicat cap font externa. No s’ha fet cap fetch.</p>
            )}
          </section>

          <section className="panel printable">
            <h3>Resum imprimible</h3>
            <pre>{printableSummary}</pre>
          </section>
        </section>
      )}
    </main>
  );
}
