import {SourceResponse} from "@/api/orag-client";
import {getFileContent} from "@/services/OragApiService";

export type SourceProps = {
    sources: SourceResponse[]
    onLoadContent: (content: string) => void
}


export function Sources(props: SourceProps) {

    const { sources } = props;

    return (
        <div className="inline-flex gap-5 mx-2 max-w-full overflow-auto mb-5 pb-2">
            {
                sources.map((source, i) =>
                    <div key={i} className="p-2 inline-flex gap-5 border-2 border-blue-800  bg-blue-500">
                        <Source source={source} onLoadContent={content => props.onLoadContent(content)} />
                    </div>)
            }
        </div>
    )
}

function Source(props: {source: SourceResponse, onLoadContent: (content: string) => void}) {
    const {source, onLoadContent} = props;

    async function getFile(file: string) {
        const content = await getFileContent(file);
        onLoadContent(content)
    }


    return (
        <div>
            <div className="flex justify-between">
                <div className="flex justify-start w-2/3 max-w-2/3">
                    <span className="truncate text-l font-bold">Zdroj : {source.title}</span>
                </div>
                <div className="flex justify-end items-center gap-2 w-1/3 max-w-1/3">
                    <span className="inline-flex items-center rounded-full bg-zinc-800 px-2 py-0.5 text-xs font-medium text-zinc-300">
                        {source.content_type}
                    </span>

                    <span className="inline-flex items-center rounded-full bg-blue-950 px-2 py-0.5 text-xs font-medium text-blue-300">
                        {source.score.toFixed(4)}
                    </span>
                </div>
            </div>
            <div className="overflow-auto text-xs">{source.text}</div>
            <a className="text-xs text-zinc-400 hover:text-yellow-200 cursor-pointer" onClick={() => getFile(source.source)}>{source.source}[{source.chunk_index}]</a>
        </div>
    )
}