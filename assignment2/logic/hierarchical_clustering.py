from assignment2.models import Blog, WordCount, Word
from shared_logic.distance_calculations import pearson


class Cluster:
    def __init__(self, right, left=None, distance=None, parent=None):
        self.right = right
        self.left = left
        self.parent = parent
        self.word_counts = dict()
        self.distance = distance

    @property
    def is_leaf(self):
        return self.right is not None and self.left is None


def iterate():
    clusters = []
    words_ids = [word.id for word in Word.objects.all()]
    for blog in Blog.objects.all():
        leaf_cluster = Cluster(blog)

        for word_count in WordCount.objects.filter(blog=blog):
            leaf_cluster.word_counts[word_count.word_id] = word_count.count

        clusters.append(leaf_cluster)

    calculations = 0

    while len(clusters) > 1:
        closest = -1

        inner_clusters = clusters.copy()
        for cluster_a in clusters:
            inner_clusters.remove(cluster_a)
            for cluster_b in inner_clusters:
                distance = _calculate_distance(words_ids, cluster_a.word_counts, cluster_b.word_counts)

                calculations += 1

                if distance > closest:
                    closest = distance
                    a = cluster_a
                    b = cluster_b

        new_cluster = _merge(words_ids, a, b, distance)
        clusters.append(new_cluster)
        clusters.remove(a)
        clusters.remove(b)

    return clusters


def _merge(words_ids, cluster_a, cluster_b, distance):
    cluster_p = Cluster(cluster_a, cluster_b, distance)
    cluster_a.parent = cluster_p
    cluster_b.parent = cluster_p

    for word_id in words_ids:
        cluster_p.word_counts[word_id] = (cluster_a.word_counts.get(word_id, 0) + cluster_b.word_counts.get(word_id, 0)) / 2

    return cluster_p


def _calculate_distance(words_ids, word_counts_a, word_counts_b):
    word_counts = []
    for word_id in words_ids:
        word_counts.append((word_counts_a.get(word_id, 0), word_counts_b.get(word_id, 0)))

    return pearson(word_counts)
