export type ChatProps = {
    isLoading?: boolean;
    question: string;
    onQuestionChange: (question: string) => void;
    answer: string;
    askQuestion?: () => void;
}

export function ChatComponent(props: ChatProps) {
    const {question, onQuestionChange, answer, isLoading, askQuestion} = props;

    return (<div>
        <textarea
            className="mt-2 min-h-28 w-full rounded-lg border border-zinc-700 bg-zinc-950 p-3 text-zinc-100 outline-none focus:border-blue-500"
            value={question}
            onChange={(event) => onQuestionChange(event.target.value)}
        />

        <button
            className="mt-3 rounded-lg bg-blue-600 px-4 py-2 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
            onClick={askQuestion}
            disabled={isLoading || !question.trim()}
        >
            {isLoading ? "Pýtam sa..." : "Spýtať sa"}
        </button>

        <p className="mt-3 whitespace-pre-wrap text-zinc-100">{answer}</p>
    </div>);
}