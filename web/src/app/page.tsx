"use client";

import {useMemo, useState} from "react";
import {AskRequest, OragClient, SourceResponse} from "@/api/orag-client";
import { askStream } from "@/api/ask-stream";

export type StreamSource = SourceResponse;

export default function Home() {
  const [question, setQuestion] = useState("Ako zálohujem PostgreSQL databázu?");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<SourceResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const client = useMemo(() => new OragClient("http://127.0.0.1:8000"), []);


  async function askQuestion() {
    setIsLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {

      await askStream({
        question,
        topK: 5,
        onSources: (newSources) => {
          setSources(newSources);
        },
        onToken: (token) => {
          setAnswer((currentAnswer) => currentAnswer + token);
        },
        onDone: () => {
          setIsLoading(false);
        },
        onError: (message) => {
          setError(message);
          setIsLoading(false);
        },
      });
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  }

  return (
      <main className="min-h-screen bg-zinc-950 text-zinc-100">
        <div className="mx-auto flex max-w-4xl flex-col gap-6 px-6 py-10">
          <header>
            <h1 className="text-3xl font-bold">ORAG</h1>
            <p className="mt-2 text-zinc-400">
              Lokálny RAG nad poznámkami a obrázkami
            </p>
          </header>

          <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
            <label className="block text-sm font-medium text-zinc-300">
              Otázka
            </label>

            <textarea
                className="mt-2 min-h-28 w-full rounded-lg border border-zinc-700 bg-zinc-950 p-3 text-zinc-100 outline-none focus:border-blue-500"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
            />

            <button
                className="mt-3 rounded-lg bg-blue-600 px-4 py-2 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
                onClick={askQuestion}
                disabled={isLoading || !question.trim()}
            >
              {isLoading ? "Pýtam sa..." : "Spýtať sa"}
            </button>

            {error && (
                <p className="mt-3 rounded-lg border border-red-800 bg-red-950 p-3 text-red-200">
                  {error}
                </p>
            )}
          </section>

          {answer && (
              <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
                <h2 className="text-xl font-semibold">Odpoveď</h2>
                <p className="mt-3 whitespace-pre-wrap text-zinc-100">{answer}</p>
              </section>
          )}

          {sources.length > 0 && (
              <section className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
                <h2 className="text-xl font-semibold">Zdroje</h2>

                <div className="mt-3 flex flex-col gap-3">
                  {sources.map((source, index) => (
                      <article
                          key={`${source.source}-${source.chunk_index}-${index}`}
                          className="rounded-lg border border-zinc-800 bg-zinc-950 p-3"
                      >
                        <div className="flex items-center justify-between gap-4">
                          <h3 className="font-medium">{source.title}</h3>
                          <span className="rounded bg-zinc-800 px-2 py-1 text-xs text-zinc-300">
                      {source.content_type} · {source.score.toFixed(4)}
                    </span>
                        </div>

                        <p className="mt-1 text-sm text-zinc-500">
                          {source.source} · chunk {source.chunk_index}
                        </p>

                        <p className="mt-3 line-clamp-4 text-sm text-zinc-300">
                          {source.text}
                        </p>
                      </article>
                  ))}
                </div>
              </section>
          )}
        </div>
      </main>
  );
}