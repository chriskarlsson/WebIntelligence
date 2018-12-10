from assignment3.logic.data_store import get_data
from assignment3.models import WordCount, Page, Word


class Result:
    word_frequency_score_normalizer = 0
    document_location_score_normalizer = 0
    page_rank_score_normalizer = 0

    def __init__(self, title, page_rank_score):
        self.title = title
        self.word_frequency_score = 0
        self.document_location_score = 0
        self.page_rank_score = page_rank_score

    @property
    def total_score(self):
        return self.word_frequency_score / Result.word_frequency_score_normalizer + \
               0.8 * Result.document_location_score_normalizer / self.document_location_score + \
               0.5 * self.page_rank_score / Result.page_rank_score_normalizer


def search(query, number_of_results):
    results = []

    word_identifiers, word_counts, pages = get_data()

    query_word_identifiers = []
    for word in query.split():
        word_id = word_identifiers.get(word)
        if word_id is not None:
            query_word_identifiers.append(word_id)

    for page in pages:
        result = Result(page.title, page.page_rank_score)

        # page_word_counts = [word_count for word_count in word_counts if word_count.page_id == page.id]
        page_word_counts = word_counts.get(page.id)
        page_word_query_counts = []
        for word_id in query_word_identifiers:
            page_word_query_count = page_word_counts.get(word_id)
            if page_word_query_count is not None:
                page_word_query_counts.append(page_word_query_count)

        result.word_frequency_score = sum(word_count.count for word_count in page_word_query_counts)
        result.document_location_score = sum(word_count.location_score for word_count in page_word_query_counts) + \
                                         (len(query_word_identifiers)-len(page_word_query_counts)) * 100000

        results.append(result)

    Result.word_frequency_score_normalizer = max(result.word_frequency_score for result in results)
    Result.document_location_score_normalizer = min(result.document_location_score for result in results)
    Result.page_rank_score_normalizer = max(result.page_rank_score for result in results)

    return sorted(results, key=lambda x: x.total_score, reverse=True)[:number_of_results]
