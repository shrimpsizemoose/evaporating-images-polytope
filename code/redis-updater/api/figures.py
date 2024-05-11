def draw_glider():
    K = "black"
    _ = None

    coords = [
        [_, K, _, _, _],
        [_, _, K, K, _],
        [_, K, K, _, _],
    ]

    return coords


def draw_moose():

    P = "pink"
    K = "black"
    W = "#904007"
    Y = "#d0925e"
    _ = None

    coords = [
        [_, Y, _, _, _, _, _, _, _, _, _, _, Y, _],
        [Y, _, _, Y, _, _, _, _, _, _, Y, _, _, Y],
        [Y, Y, Y, _, _, _, _, _, _, _, _, Y, Y, Y],
        [_, Y, Y, _, _, _, _, _, _, _, _, Y, Y, Y],
        [_, Y, Y, _, _, W, _, _, _, W, _, Y, Y, _],
        [Y, Y, Y, Y, W, W, W, W, W, Y, Y, Y, Y, Y],
        [_, _, _, _, W, K, W, K, W, Y, _, _, _, _],
        [W, W, W, W, W, W, W, W, W, W, _, _, _, _],
        [W, W, W, W, W, W, W, W, W, W, _, _, _, _],
        [W, P, W, P, W, W, W, W, W, W, _, _, _, _],
        [W, W, W, W, W, W, W, W, W, W, _, _, _, _],
        [W, W, W, W, W, W, W, W, W, W, _, _, _, _],
        [W, W, W, W, W, W, W, W, W, W, W, W, W, W],
        [_, _, _, _, W, W, W, W, W, W, W, W, W, W],
        [_, _, _, _, W, W, W, W, W, W, W, W, W, W],
        [_, _, _, _, W, W, W, W, W, W, W, W, W, W],
        [_, _, _, _, _, W, _, W, _, _, _, W, _, W],
        [_, _, _, _, _, W, _, W, _, _, _, W, _, W],
    ]

    return coords
