import {FileRequest, OragClient} from "@/api/orag-client";
import { API_BASE_URL } from "@/lib/api-config";

function createOragClient() {
    return new OragClient(API_BASE_URL, {
        fetch: (url, init) => fetch(url, init),
    });
}

export async function getStats() {
    const client = createOragClient();
    return client.stats();
}

export async function getFileContent(file: string) {
    const client = createOragClient();
    return client.view_file_content(new FileRequest({ file }));
}