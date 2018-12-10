from os import path, walk

from django.db import transaction

from assignment3.models import Page, Word, WordCount


def load_data():
    if Page.objects.count() > 0:
        return

    data_dir = path.join(path.dirname(__file__), 'data')
    word_dir = path.join(data_dir, 'Words')
    link_dir = path.join(data_dir, 'Links')

    page_rank_iterations = 20

    # Pages, words and word counts
    with transaction.atomic():
        word_ids = {}
        for directory_path, _, file_names in walk(word_dir):
            for file_name in file_names:
                page = Page.objects.create(title=file_name)
                word_counts = {}
                with open(path.join(directory_path, file_name), 'r') as file:
                    for line in file:
                        for location, string in enumerate(line.split()):
                            word_id = word_ids.get(string)
                            if word_id is None:
                                word = Word.objects.create(word=string)
                                word_id = word.id
                                word_ids[string] = word_id
                            word_count = word_counts.get(word_id, _WordCount())
                            word_count.word_occasion(location + 1)
                            word_counts[word_id] = word_count

                for word_id, word_count in word_counts.items():
                    WordCount.objects.create(page=page, word_id=word_id, count=word_count.count, location_score=word_count.location_score)

    # Links
    with transaction.atomic():
        pages = {}
        for page in Page.objects.all():
            pages[page.title] = page

        links = []

        for directory_path, _, file_names in walk(link_dir):
            for file_name in file_names:
                source_page = pages.get(file_name)
                if source_page is not None:
                    with open(path.join(directory_path, file_name), 'r') as links:
                        source_page.outward_links = 0
                        for link in links:
                            source_page.outward_links += 1
                            link = link.lstrip('/wiki/').rstrip()
                            target_page = pages.get(link)
                            if target_page is not None:
                                links.append(_Link(source_page.id, target_page.id))

        for _, page in pages.items():
            page.save()

    # Page ranks
    with transaction.atomic():
        pages = {}
        page_ranks = []
        for page in Page.objects.all():
            pages[page.id] = page
            page_rank = _PageRank(page.id)
            for link in (link for link in links if link.target_id == page.id):
                page_rank.link_page_ids.append(link.source_id)

            page_ranks.append(page_rank)

        for _ in range(page_rank_iterations):
            for page_rank in page_ranks:
                for source_page_id in page_rank.link_page_ids:
                    source_page = pages[source_page_id]
                    page_rank.page_rank_score += source_page.page_rank_score / source_page.outward_links

            for page_rank in page_ranks:
                pages[page_rank.page_id].page_rank_score = page_rank.page_rank_score * 0.85 + 0.15
                page_rank.page_rank_score = 0

        for _, page in pages.items():
            page.save()


class _PageRank:
    def __init__(self, page_id):
        self.page_id = page_id
        self.link_page_ids = []
        self.page_rank_score = 0


class _WordCount:
    def __init__(self):
        self.count = 0
        self.location_score = 0

    def word_occasion(self, word_location):
        self.count += 1
        if self.location_score == 0:
            self.location_score = word_location


class _Link:
    def __init__(self, source_id, target_id):
        self.source_id = source_id
        self.target_id = target_id
