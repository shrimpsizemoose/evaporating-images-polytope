import itertools
import os
import random

import redis

from api.figures import draw_glider, draw_moose


def build_coords_data(coords, shiftX=0, shiftY=0, evaporate=False):
    data = {}
    nr = len(coords)
    nc = len(coords[0])
    for row, col in itertools.product(range(nr), range(nc)):
        if (color := coords[row][col]) is not None:
            y, x = row + shiftY, col + shiftX
            draw = not evaporate or random.random() < 0.5
            data[y, x] = {
                'x': x,
                'y': y,
                'color': color,
                'draw': int(draw),
            }

    return data


def update_coords_in_redis(url, evaporate=False):
    r = redis.from_url(url)
    r.flushdb()

    glider = draw_glider()
    moose = draw_moose()

    # moose can go
    pixels = build_coords_data(moose, shiftX=7, shiftY=5)
    for (y, x), v in pixels.items():
        key = f'coords:{y}:{x}'
        r.hset(key, mapping=v)
        if evaporate:
            r.expire(key, int(10 * random.random()))

    # the glider stays
    pixels = build_coords_data(glider, shiftY=1)
    for (y, x), v in pixels.items():
        key = f'coords:{y}:{x}'
        r.hset(key, mapping=v)


if __name__ == '__main__':
    url = os.getenv('REDIS_URL')
    print(url)
    update_coords_in_redis(url=url, evaporate=True)
