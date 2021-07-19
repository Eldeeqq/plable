def overlap_fitness(vector: list[int], parallels):
    """
    Returns number of overlaping events
    """
    final = []
    used = 0
    
    for cls in parallels.values():
        for parallel_list in cls.values():
            final.append(parallel_list[vector[used]])
            used +=1

    hits = 0
    for i, x in enumerate(final):
        for y in final[i + 1 :]:
            if not x.collision_free(y):
                hits += 1

    return hits,