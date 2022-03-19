import numpy as np


def tri_coords(a, x0, y0, up):
    """Create coordinates for a triangle
    a           = side length
    (x0, y0)    = Center of triangle
    up          = direction of triangle
    """
    h = a * np.sqrt(3) / 2
    if up:
        x = np.array([-1 / 2, 1 / 2, 0]) + x0
        y = np.array([-h / 2, -h / 2, h / 2]) + y0
    else:
        x = np.array([-1 / 2, 1 / 2, 0]) + x0
        y = np.array([h / 2, h / 2, -h / 2]) + y0
    return (x, y)


def row(a, n_row, height):
    """Create (x, y) coordinates for a row of triangles.
    a       = side length
    n_row   = number of triangles in this row
    height  = 
    """
    h = a * np.sqrt(3) / 2
    xi = np.arange(n_row)
    x = (xi - n_row // 2) * a / 2
    if height > 0:
        y = np.zeros(x.shape) + (height * 2 - 1) * h / 2
    else:
        y = np.zeros(x.shape) + (height * 2 + 1) * h / 2
    ud = (xi % 2).astype("bool")
    if height > 0:
        ud = ~ud
    return (x, y, ud)


def classic(a=1):
    """Create the classic (mkI) layout.
    """
    x0, y0 = [], []
    xs, ys = [], []
    px_per_row = [5, 7, 7, 5]
    row_offset = [2, 1, -1, -2]

    for ppr, ro in zip(px_per_row, row_offset):
        for x0i, y0i, ud in zip(*row(a, ppr, ro)):
            x0.append(x0i)
            y0.append(y0i)
            (x, y) = tri_coords(a, x0i, y0i, ud)
            xs.append(x)
            ys.append(y)

    return (x0, y0, xs, ys)


def extended(a=1):
    """Create the extended (mkII) layout.
    """
    x0, y0 = [], []
    xs, ys = [], []
    px_per_row = [19, 21, 23, 23, 21, 19]
    row_offset = [3, 2, 1, -1, -2, -3]

    for ppr, ro in zip(px_per_row, row_offset):
        for x0i, y0i, ud in zip(*row(a, ppr, ro)):
            x0.append(x0i)
            y0.append(y0i)
            (x, y) = tri_coords(a, x0i, y0i, ud)
            xs.append(x)
            ys.append(y)

    return (x0, y0, xs, ys)


def shift(values, shift):
    """Shift a layout of values left/right in the extended layout.
    """
    px_per_row = [0, 19, 21, 23, 23, 21, 19]
    px_cumsum = np.cumsum(np.array(px_per_row))
    new_values = []
    for v in values:
        row = np.where(v < px_cumsum)[0][0]
        v2 = v + shift
        if px_cumsum[row-1] <= v2 < px_cumsum[row]:
            new_values.append(v2)
    return new_values
