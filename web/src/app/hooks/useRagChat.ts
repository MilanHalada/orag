"use client";

import { useState } from "react";

import {askStream, StreamSource} from "@/api/ask-stream";

const DEFAULT_TOP_K = 5;

export function useRagChat() {
    const [question, setQuestion] = useState("Kedy treba spravit postrek broskyn?");
    const [answer, setAnswer] = useState("");
    const [sources, setSources] = useState<StreamSource[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    async function askQuestion() {
        if (!question.trim()) {
            return;
        }

        setIsLoading(true);
        setError("");
        setAnswer("");
        setSources([]);

        try {
            await askStream({
                question,
                topK: DEFAULT_TOP_K,
                onSources: setSources,
                onToken: (token) => {
                    setAnswer((currentAnswer) => currentAnswer + token);
                },
                onError: (message) => {
                    setError(message);
                },
            });
        } catch (error) {
            setError(error instanceof Error ? error.message : "Unknown error");
        } finally {
            setIsLoading(false);
        }
    }

    return {
        question,
        setQuestion,
        answer,
        sources,
        isLoading,
        error,
        askQuestion,
    };
}