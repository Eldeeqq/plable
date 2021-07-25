from re import A
from typing import List
from datetime import datetime, timedelta
from plable.components import Parallel


def overlap(a, b):
    """
    Checks whether two events overlap
    """
    start_a, end_a = a
    start_b, end_b = b

    # if times overlap -> collision
    return (start_a <= start_b <= end_a) or (start_b <= start_a <= end_b)


def decode(sample, parallels):
    final: List[Parallel] = []
    used = 0

    for cls in parallels.values():
        for parallel_list in cls.values():
            final.append(parallel_list[sample[used]])
            used += 1
    return final


def overlap_fitness(vector: List[int], parallels):
    """
    Returns number of overlaping events
    """
    final: List[Parallel] = decode(vector, parallels)
    hits: int = 0
    for i, x in enumerate(final):
        for y in final[i + 1 :]:
            if not x.collision_free(y):
                hits += 1

    return (hits,)


def minutes_between_classes(vector: List[int], parallels):
    parse_time = lambda x: datetime.strptime(x, "%H:%M:%S")
    final: List[Parallel] = decode(vector, parallels)

    event_per_day_even = {x: [] for x in range(1, 6)}
    event_per_day_odd = {x: [] for x in range(1, 6)}

    for parallel in final:
        # if parallel._course == 'BI-LIN':
        #     print(parallel._slots)
        for event in parallel._slots:
            day, parity, room, start, end = event

            if parity != "ODD":  # even, both
                event_per_day_even[int(day)].append((parse_time(start), parse_time(end)))

            if parity != "EVEN":  # odd, both
                event_per_day_odd[int(day)].append((parse_time(start), parse_time(end)))

    total = 0
    collisions = 0
    for day in event_per_day_even.values():
        if len(day) < 2:
            continue
        day.sort()
        for i in range(len(day) - 1):
            if overlap(day[i], day[i + 1]):
                collisions += 1
            else:
                total += abs((day[i][1] - day[i + 1][0]).seconds // 60 % 60)

    for day in event_per_day_odd.values():
        if len(day) < 2:
            continue
        day.sort()
        for i in range(len(day) - 1):
            if overlap(day[i], day[i + 1]):
                collisions += 1
            else:
                total += abs((day[i][1] - day[i + 1][0]).seconds // 60 % 60)

    # print(f'{collisions =}, {total = }')
    return collisions, total


names = ["Least collisions", "Time between classes"]
functions = [overlap_fitness, minutes_between_classes]
weights = [(-1,), (-1, -1)]
