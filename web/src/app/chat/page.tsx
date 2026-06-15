"use client"

import {ChatComponent} from "@/components/chat/ChatComponent";
import {Sources} from "@/components/chat/Sources";
import {useRagChat} from "@/app/hooks/useRagChat";
import {SourceResponse} from "@/api/orag-client";
import {useState} from "react";
import {SourceContentDialog} from "@/components/chat/SourceContentDialog";
export default function ChatPage() {

    const {question, setQuestion, answer, sources, isLoading, error, askQuestion} = useRagChat();

    const [sourceContent, setSourceContent] = useState<string | null>(null);


    return (
        <div>
            {error ? <div className="text-red-600">{error}</div> : <></>}

            <Sources
                sources={sources as SourceResponse[]}
                onLoadContent={setSourceContent} />

            <ChatComponent
                question={question}
                onQuestionChange={setQuestion}
                askQuestion={askQuestion}
                isLoading={isLoading}
                answer={answer} />

            {sourceContent &&
            <SourceContentDialog
                content={sourceContent}
                onClose={() => setSourceContent(null)}
            />}
        </div>
    )

    function sourceContentDialog(content: string) {


        return <div className="p-2 border-2 border-blue-800 bg-blue-500">{content}</div>
    }

}

