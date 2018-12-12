from os import path, walk


def get_data():
    if len(get_data.__dict__) == 0:
        data_dir = path.join(path.dirname(__file__), '..', 'data')
        word_dir = path.join(data_dir, 'Words')
        link_dir = path.join(data_dir, 'Links')

        page_rank_iterations = 20

        # Pages, words and word counts
        pages = {}
        get_data.word_ids = {}
        get_data.word_counts_by_page_id = {}
        for directory_path, _, file_names in walk(word_dir):
            for file_name in file_names:
                page = Page(file_name)
                pages[page.title] = page
                word_counts = {}
                with open(path.join(directory_path, file_name), 'r') as file:
                    for line in file:
                        for location, string in enumerate(line.split()):
                            word_id = get_data.word_ids.get(string)
                            if word_id is None:
                                word = Word(string)
                                word_id = word.id
                                get_data.word_ids[string] = word_id
                            word_count = word_counts.get(word_id)
                            if word_count is None:
                                word_count = WordCount(page.id, word_id)
                                word_counts[word_id] = word_count

                            word_count.word_occasion(location + 1)

                get_data.word_counts_by_page_id[page.id] = word_counts

        # Links
        links = []
        for directory_path, _, file_names in walk(link_dir):
            for file_name in file_names:
                source_page = pages.get(file_name)
                if source_page is not None:
                    with open(path.join(directory_path, file_name), 'r') as link_file:
                        source_page.outward_links = 0
                        for link in link_file:
                            source_page.outward_links += 1
                            link = link.lstrip('/wiki/').rstrip()
                            target_page = pages.get(link)
                            if target_page is not None:
                                links.append(_Link(source_page.id, target_page.id))

        # Page ranks
        get_data.pages_by_id = {}
        page_ranks = []
        for _, page in pages.items():
            get_data.pages_by_id[page.id] = page
            page_rank = _PageRank(page.id)
            for link in (link for link in links if link.target_id == page.id):
                page_rank.link_page_ids.append(link.source_id)

            page_ranks.append(page_rank)

        for _ in range(page_rank_iterations):
            for page_rank in page_ranks:
                for source_page_id in page_rank.link_page_ids:
                    source_page = get_data.pages_by_id.get(source_page_id)
                    if source_page is not None:
                        page_rank.page_rank_score += source_page.page_rank_score / source_page.outward_links

            for page_rank in page_ranks:
                page = get_data.pages_by_id.get(page_rank.page_id)
                if page is not None:
                    page.page_rank_score = page_rank.page_rank_score * 0.85 + 0.15
                page_rank.page_rank_score = 0

    return get_data.word_ids, get_data.word_counts_by_page_id, get_data.pages_by_id


class _PageRank:
    def __init__(self, page_id):
        self.page_id = page_id
        self.link_page_ids = []
        self.page_rank_score = 0


class _Link:
    def __init__(self, source_id, target_id):
        self.source_id = source_id
        self.target_id = target_id


class Page:
    id_max = 0

    def __init__(self, title):
        self.title = title
        self.page_rank_score = 1
        self.outward_links = 0
        Page.id_max += 1
        self.id = Page.id_max


class Word:
    id_max = 0

    def __init__(self, word):
        self.word = word
        Word.id_max += 1
        self.id = Word.id_max


class WordCount:
    id_max = 0

    def __init__(self, page_id, word_id):
        self.page_id = page_id
        self.word = word_id
        self.count = 0
        self.location_score = 0
        WordCount.id_max += 1
        self.id = WordCount.id_max

    def word_occasion(self, word_location):
        self.count += 1
        if self.location_score == 0:
            self.location_score = word_location
