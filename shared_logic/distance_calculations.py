from math import sqrt


def euclidean(distances):
    total_sum = 0
    n = 0

    for distance in distances:
        total_sum += (distance[0] - distance[1])**2
        n += 1

    return 0 if n == 0 else 1/(1 + total_sum)


def pearson(distances):
    sum_1 = 0
    sum_2 = 0
    sum_1_sq = 0
    sum_2_sq = 0
    p_sum = 0
    n = 0

    for distance in distances:
        sum_1 += distance[0]
        sum_2 += distance[1]
        sum_1_sq += distance[0]**2
        sum_2_sq += distance[1]**2
        p_sum += distance[0] * distance[1]
        n += 1

    if n == 0:
        return 0

    num = p_sum - (sum_1 * sum_2 / n)
    den = sqrt((sum_1_sq - sum_1**2 / n) * (sum_2_sq - sum_2**2 / n))

    return num / den
