import math

from openai import OpenAI
from embeddings import get_embedding
from models import IndexedChunk, Chunk


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Computes the cosine similarity between two vectors.

    :param a: The first vector.
    :param b: The second vector.
    :return: The cosine similarity score.

    """

    # zip(a, b) - this creates a list of tuples for iteration, where each tuple contains the corresponding elements of a and b.
    #         So when
    #         a = [1, 2, 3] - vector a with 3 elements - dimensions
    #         b = [10, 20, 30] - vector b with 3 elements - dimensions
    #         result is [(1, 10), (2, 20), (3, 30)]
    #
    #         So for x, y in zip(a, b) takes corresponding elements from a and b and puts them into x and y.
    #
    #         and x * y is simple multiplication of corresponding elements.
    #
    #         and sum(x * y for x, y in zip(a, b)) is sum of all these products - this is the dot product. Math stuff.
    #
    #         length_a = math.sqrt(sum(x * x for x in a)) - this is the length of vector a. All elements are squared and then summed, and then square root is taken.
    #
    #         length_b = math.sqrt(sum(y * y for y in b)) - same as above, but for vector b.
    #
    #         final result is dot_product / (length_a * length_b) - this is the cosine similarity - cos(angle) = dot_product / (length_a * length_b)
    #         cosine similarity is a measure of similarity between two vectors, ranging from -1 (opposite direction) to 1 (same direction), with 0 indicating orthogonality.
    #
    #         for a and b the dot product is 140. length_a is sqrt(14) = 3.74165, length_b is sqrt(1400 = 37.4165). Multiplied it is ~140. So cosine similarity is ~1.

    dot_product = sum(x * y for x, y in zip(a, b))

    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))

    if length_a == 0 or length_b == 0:
        return 0.0

    return dot_product / (length_a * length_b)


def search(
        client: OpenAI,
        indexed_chunks: list[IndexedChunk],
        query: str,
        top_k: int = 3,
) -> list[tuple[float, Chunk]]:
    query_embedding = get_embedding(client, query)

    results: list[tuple[float, Chunk]] = []

    for indexed_chunk in indexed_chunks:
        score = cosine_similarity(query_embedding, indexed_chunk.embedding)
        results.append((score, indexed_chunk.chunk))

    results.sort(reverse=True, key=lambda item: item[0])

    return results[:top_k]