export type StreamSource = {
    title: string;
    source: string;
    chunk_index: number;
    content_type: string;
    score: number;
    text: string;
};

type AskStreamParams = {
    question: string;
    topK: number;
    onSources: (sources: StreamSource[]) => void;
    onToken: (token: string) => void;
    onDone?: () => void;
    onError?: (message: string) => void;
};

type SseEvent = {
    event: string;
    data: string;
};

function parseSseBlock(block: string): SseEvent | null {
    const lines = block.split("\n");

    let event = "";
    const dataLines: string[] = [];

    for (const line of lines) {
        if (line.startsWith("event:")) {
            event = line.slice("event:".length).trim();
            continue;
        }

        if (line.startsWith("data:")) {
            dataLines.push(line.slice("data:".length).trim());
        }
    }

    if (!event) {
        return null;
    }

    return {
        event,
        data: dataLines.join("\n"),
    };
}

function handleSseEvent(
    sseEvent: SseEvent,
    handlers: Pick<AskStreamParams, "onSources" | "onToken" | "onDone" | "onError">,
) {
    if (sseEvent.event === "sources") {
        const sources = JSON.parse(sseEvent.data) as StreamSource[];
        handlers.onSources(sources);
        return;
    }

    if (sseEvent.event === "token") {
        const token = JSON.parse(sseEvent.data) as string;
        handlers.onToken(token);
        return;
    }

    if (sseEvent.event === "done") {
        handlers.onDone?.();
        return;
    }

    if (sseEvent.event === "error") {
        const payload = JSON.parse(sseEvent.data) as { message?: string };
        handlers.onError?.(payload.message ?? "Unknown stream error");
    }
}

export async function askStream({
                                    question,
                                    topK,
                                    onSources,
                                    onToken,
                                    onDone,
                                    onError,
                                }: AskStreamParams): Promise<void> {
    const response = await fetch("http://127.0.0.1:8000/ask/stream", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
        },
        body: JSON.stringify({
            question,
            top_k: topK,
        }),
    });

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }

    if (!response.body) {
        throw new Error("Response body is empty.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let buffer = "";

    while (true) {
        const { value, done } = await reader.read();

        if (done) {
            break;
        }

        buffer += decoder.decode(value, { stream: true });

        const blocks = buffer.split("\n\n");
        buffer = blocks.pop() ?? "";

        for (const block of blocks) {
            const parsedEvent = parseSseBlock(block);

            if (!parsedEvent) {
                continue;
            }

            handleSseEvent(parsedEvent, {
                onSources,
                onToken,
                onDone,
                onError,
            });
        }
    }

    // Ak ostal posledný event bez finálneho \n\n, skús ho ešte spracovať.
    const remaining = buffer.trim();

    if (remaining) {
        const parsedEvent = parseSseBlock(remaining);

        if (parsedEvent) {
            handleSseEvent(parsedEvent, {
                onSources,
                onToken,
                onDone,
                onError,
            });
        }
    }
}