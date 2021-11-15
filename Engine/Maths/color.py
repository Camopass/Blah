import math


# Stackoverflow time hehehehehehehe
def lerp(a, b, t):
    return a * (1 - t) + b * t


def rgb_lerp(color_a, color_b, t):
    return lerp(color_a[0], color_b[0], t), lerp(color_a[1], color_b[1], t), lerp(color_a[2], color_b[2], t)


# https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
def hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h * 6.)  # XXX assume int() truncates!
    f = (h * 6.) - i
    p, q, t = v * (1. - s), v * (1. - s * f), v * (1. - s * (1. - f))
    i %= 6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)
