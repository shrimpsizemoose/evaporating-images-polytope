def read_grid(r):
    nr = 50
    nc = 50
    grid = set()
    for y in range(nr + 1):
        for x in range(nc + 1):
            key = f'coords:{y}:{x}'
            if r.exists(key):
                grid.add((y, x))
    return grid


def neighbors(y, x):
    yield y - 1, x - 1
    yield y - 1, x
    yield y - 1, x + 1
    yield y, x + 1
    yield y, x - 1
    yield y + 1, x + 1
    yield y, x + 1
    yield y + 1, x + 1


def iter_grid(grid):
    nr, nc = 50, 50
    new = set()
    for y in range(nr + 1):
        for x in range(nc + 1):
            live = 0
            for yy, xx in neighbors(y, x):
                if (yy, xx) in grid:
                    live += 1
            if (y, x) in grid and live in (2, 3):
                new.add((y, x))
            elif (y, x) not in grid and live == 3:
                new.add((y, x))
    return new


def write_grid(r, grid):
    nr = 50
    nc = 50
    for y in range(nr + 1):
        for x in range(nc + 1):
            if (y, x) in grid:
                key = f'coords:{y}:{x}'
                value = {
                    'x': x,
                    'y': y,
                    'color': 'black',
                    'draw': 1,
                }
                r.hset(key, mapping=value)
