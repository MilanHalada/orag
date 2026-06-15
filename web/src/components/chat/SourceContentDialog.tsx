import {MarkdownContent} from "@/components/common/MarkdownContent";

type SourceContentDialogProps = {
    content: string;
    onClose: () => void;
};

export function SourceContentDialog({
        content,
        onClose,
    }: SourceContentDialogProps) {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
            <div className="flex max-h-[80vh] w-full max-w-4xl flex-col rounded-xl border border-zinc-700 bg-zinc-950 shadow-xl">
                <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
                    <h2 className="text-lg font-semibold text-zinc-100">
                        Zdrojový obsah
                    </h2>

                    <button
                        type="button"
                        onClick={onClose}
                        className="rounded-md px-2 py-1 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100"
                    >
                        Zavrieť
                    </button>
                </div>

                <div className="overflow-auto p-4">
          <pre className="whitespace-pre-wrap wrap-break-words text-sm text-zinc-200">
            <MarkdownContent content={content} />
          </pre>
                </div>
            </div>
        </div>
    );
}