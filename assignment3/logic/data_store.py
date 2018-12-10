from assignment3.models import Word, WordCount, Page


def get_data():
    if len(get_data.__dict__) == 0:
        get_data.word_identifiers = {}
        for word in list(Word.objects.all()):
            get_data.word_identifiers[word.word] = word.id

        get_data.word_counts = {}
        for word_count in list(WordCount.objects.all()):
            items = get_data.word_counts.get(word_count.page_id)
            if items is None:
                get_data.word_counts[word_count.page_id] = {word_count.word_id: word_count}
            else:
                items[word_count.word_id] = word_count

        get_data.pages = list(Page.objects.all())

    return get_data.word_identifiers, get_data.word_counts, get_data.pages
