from functools import reduce


def calculate_pattern(filename):
    # see constructPages in viewer_image_1.2.5_2018-10-05.js

    t = reduce(lambda acc, c: acc + ord(c), list(filename), 0)
    return t % 4 + 1


def calculate_moves(width, height, tileW, tileH, pattern):
    # see a3f in viewer_image_1.2.5_2018-10-05.js

    cols = width // tileW
    rows = height // tileH
    remW = width % tileW   # width remainder
    remH = height % tileH  # height remainder
    moves = []

    offsetX = cols - 43 * pattern % cols
    if offsetX % cols == 0:
        offsetX = (cols - 4) % cols
    if offsetX == 0:
        offsetX = cols - 1

    offsetY = rows - 47 * pattern % rows
    if offsetY % rows == 0:
        offsetY = (rows - 4) % rows
    if offsetY == 0:
        offsetY = rows - 1

    if 0 < remW and 0 < remH:
        srcX = offsetX * tileW
        srcY = offsetY * tileH
        moves.append((srcX, srcY, srcX, srcY, remW, remH))

    if 0 < remH:
        for col_index in range(cols):
            u = calcXCoordinateXRest_(col_index, cols, pattern)
            v = calcYCoordinateXRest_(u, offsetX, offsetY, rows, pattern)
            destX = calcPositionWithRest_(u, offsetX, remW, tileW)
            destY = v * tileH
            srcX = calcPositionWithRest_(col_index, offsetX, remW, tileW)
            srcY = offsetY * tileH
            moves.append((srcX, srcY, destX, destY, tileW, remH))

    if 0 < remW:
        for row_index in range(rows):
            v = calcYCoordinateYRest_(row_index, rows, pattern)
            u = calcXCoordinateYRest_(v, offsetX, offsetY, cols, pattern)
            destX = u * tileW
            destY = calcPositionWithRest_(v, offsetY, remH, tileH)
            srcX = offsetX * tileW
            srcY = calcPositionWithRest_(row_index, offsetY, remH, tileH)
            moves.append((srcX, srcY, destX, destY, remW, tileH))

    for col_index in range(cols):
        for row_index in range(rows):
            u = (col_index + pattern * 29 + 31 * row_index) % cols
            v = (row_index + pattern * 37 + 41 * u) % rows
            if calcXCoordinateYRest_(v, offsetX, offsetY, cols, pattern) <= u:
                w = remW
            else:
                w = 0
            if calcYCoordinateXRest_(u, offsetX, offsetY, rows, pattern) <= v:
                x = remH
            else:
                x = 0
            destX = u * tileW + w
            destY = v * tileH + x
            srcX = col_index * tileW + (remW if col_index >= offsetX else 0)
            srcY = row_index * tileH + (remH if row_index >= offsetY else 0)
            moves.append((srcX, srcY, destX, destY, tileW, tileH))

    return moves


def calcPositionWithRest_(a, b, c, d):
    return a * d + (c if a >= b else 0)


def calcXCoordinateXRest_(col_index, cols, pattern):
    return (col_index + 61 * pattern) % cols


def calcYCoordinateXRest_(a, b, c, d, pattern):
    pattern_is_odd = (pattern % 2 == 1)
    k = (pattern_is_odd if a < b else not pattern_is_odd)
    if k:
        j = c
        i = 0
    else:
        j = d - c
        i = c
    return (a + pattern * 53 + c * 59) % j + i


def calcXCoordinateYRest_(a, b, c, d, pattern):
    pattern_is_odd = (pattern % 2 == 1)
    k = (pattern_is_odd if a < c else not pattern_is_odd)
    if k:
        j = d - b
        g = b
    else:
        j = b
        g = 0
    return (a + pattern * 67 + b + 71) % j + g


def calcYCoordinateYRest_(row_index, rows, pattern):
    return (row_index + 73 * pattern) % rows
