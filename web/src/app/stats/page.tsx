"use client";

import { useEffect, useMemo, useState } from "react";

import { OragClient, StatsResponse } from "@/api/orag-client";
import { API_BASE_URL } from "@/lib/api-config";
import {getStats} from "@/services/OragApiService";

export default function StatsPage() {
    const [stats, setStats] = useState<StatsResponse | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadStats() {
            setIsLoading(true);
            setError("");

            try {
                const result = await getStats();
                setStats(result);
            } catch (error) {
                setError(error instanceof Error ? error.message : "Unknown error");
            } finally {
                setIsLoading(false);
            }
        }

        void loadStats();
    }, []);

    const {
        documents_count,
        images_count,
        chunk_count,
        indexed_chunk_count,
    } = stats ?? {};

    return (
        <div>
            {isLoading && <div>Loading...</div>}

            {error && <div>Error: {error}</div>}

            {stats && (
                <>
                    <div>Documents: {documents_count}</div>
                    <div>Images: {images_count}</div>
                    <div>Chunks: {chunk_count}</div>
                    <div>Indexed Chunks: {indexed_chunk_count}</div>
                </>
            )}
        </div>
    );
}