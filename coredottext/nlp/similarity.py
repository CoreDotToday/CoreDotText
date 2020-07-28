# -*- coding: utf-8 -*-
import scipy

def cosine_similarity(v1,v2):
    """
    compute cosine similarity of v1 to v2: (v1 dot v1)/{||v1||*||v2||)
    #100 loops, best of 3: 11.9 ms per loop
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)
    """
    # 10000 loops, best of 3: 124 µs per loop
    return 1-scipy.spatial.distance.cosine(v1, v2)