from assignment3.models import WordCount, Page, Word


class Result:
    word_frequency_score_normalizer = 0
    document_location_score_normalizer = 0
    page_rank_score_normalizer = 0

    def __init__(self, url, page_rank_score):
        self.url = url
        self.word_frequency_score = 0
        self.document_location_score = 0
        self.page_rank_score = page_rank_score

    @property
    def total_score(self):
        return self.word_frequency_score / Result.word_frequency_score_normalizer + \
               0.8 * Result.document_location_score_normalizer / self.document_location_score + \
               0.5 * self.page_rank_score / Result.page_rank_score_normalizer


def find(query, number_of_results):
    results = []
    query_word_identifiers = [word.id for word in Word.objects.all() if word in query]

    word_counts = [word_count for word_count in WordCount.objects.all() if word_count.word_id in query_word_identifiers]
    pages = Page.objects.all()
    for page in pages:
        result = Result(page.url, page.page_rank_score)

        page_word_counts = [word_count for word_count in word_counts if word_count.page_id == page.id]

        result.word_frequency_score = sum(word_count.count for word_count in page_word_counts)
        result.document_location_score = sum(word_count.location_score for word_count in page_word_counts) + \
                                         (len(query_word_identifiers)-len(page_word_counts)) * 100000

        results.append(result)

    Result.word_frequency_score_normalizer = max(result.word_frequency_score for result in results)
    Result.document_location_score_normalizer = min(result.document_location_score for result in results)
    Result.page_rank_score_normalizer = max(result.page_rank_score for result in results)

    return sorted(result.total_score for result in results)[:number_of_results]
