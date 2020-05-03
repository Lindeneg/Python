# https://en.wikipedia.org/wiki/Midpoint_circle_algorithm

from typing import Tuple, List, Optional, Any

#                (x,   y)
Vector2D = Tuple[int, int]
Vectors2D = List[Vector2D]


def get_circle_vectors(
    center: Vector2D, radius: int, fill: Optional[bool] = False
) -> Vectors2D:
    """
    Returns a list of 2-dimensional vectors approximating the perimeter of a circle
    If the optional fill argument is true, then include vectors found inside the circle

        center   : center points of the circle
        radius   : the radius of the circle
        fill     : include vectors inside the circle
    return list of vectors defining the circle

    >>> get_circle_vectors((50, 50), 2)
    [(52, 50), (50, 52), (48, 50), (50, 48), (52, 51), (49, 52), (48, 49), (51, 48), (51, 52), (48, 51), (49, 48), (52, 49)]

    >>> get_circle_vectors((25, 25), 1)
    [(26, 25), (25, 26), (24, 25), (25, 24)]

    >>> get_circle_vectors((42, 42), 1)
    [(43, 42), (42, 43), (41, 42), (42, 41)]

    >>> get_circle_vectors((42, 42), 0)
    []
    """
    circle_vectors: Vectors2D = []
    if _validate_input(center) and _is_int(radius):
        x: int = -radius
        y: int = 0
        error: int = 2 - 2 * radius
        while x < 0:
            circle_vectors.extend(_get_circle_quadrants(center, (x, y)))
            radius = error
            if radius <= y:
                y += 1
                error += y * 2 + 1
            if radius > x or error > y:
                x += 1
                error += x * 2 + 1
        if fill:
            circle_vectors.extend(_get_vectors_inside_circle(center, radius))
    return circle_vectors


def _get_circle_quadrants(center: Vector2D, current_point: Vector2D) -> Vectors2D:
    """
        center          : center points of the circle
        current_point   : current point on the circle
    return list of vectors defining a quadrant on the circle

    >>> _get_circle_quadrants((50, 50), (-2, 0))
    [(52, 50), (50, 52), (48, 50), (50, 48)]

    >>> _get_circle_quadrants((50, 50), (-1, 0))
    [(51, 50), (50, 51), (49, 50), (50, 49)]
    """
    circle_vectors: Vectors2D = []
    if _validate_input(center) and _validate_input(current_point):
        circle_vectors = [
            # I.   Quadrant
            (center[0] - current_point[0], center[1] + current_point[1]),
            # II.  Quadrant
            (center[0] - current_point[1], center[1] - current_point[0]),
            # III. Quadrant
            (center[0] + current_point[0], center[1] - current_point[1]),
            # IV.  Quadrant
            (center[0] + current_point[1], center[1] + current_point[0]),
        ]
    return circle_vectors


def _get_vectors_inside_circle(center: Vector2D, radius: int) -> Vectors2D:
    """
        center   : center points of the circle
        radius   : the radius of the circle
    return list of vectors inside the boundaries of the circle

    >>> _get_vectors_inside_circle((50, 50), 2)
    [(50, 48), (49, 49), (50, 49), (51, 49), (48, 50), (49, 50), (50, 50), (51, 50), (52, 50), (49, 51), (50, 51), (51, 51), (50, 52)]

    >>> _get_vectors_inside_circle((25, 25), 1)
    [(25, 24), (24, 25), (25, 25), (26, 25), (25, 26)]

    >>> _get_vectors_inside_circle((42, 42), 0)
    [(42, 42)]

    >>> _get_vectors_inside_circle((42, 42), "c")
    []

    >>> _get_vectors_inside_circle((42, 42, 2), "c")
    Traceback (most recent call last):
    TypeError: "center" must be an indexable type with two items, not (42, 42, 2)
    """
    circle_vectors = []
    if _validate_input(center) and _is_int(radius):
        boundary: range = range(-radius, radius + 1)
        for y in boundary:
            for x in boundary:
                if x ** 2 + y ** 2 <= radius ** 2:
                    circle_vectors.append((center[0] + x, center[1] + y))
    return circle_vectors


def _validate_input(arg: Any) -> bool:
    """
    Validate that we have an indexable object with two integer items

        arg: argument to be validated
    return true if test is passed, otherwise raise an exception

    >>> _validate_input((42, 25))
    True

    >>> _validate_input((42, 25, 53))
    Traceback (most recent call last):
    TypeError: "center" must be an indexable type with two items, not (42, 25, 53)

    >>> _validate_input(("a", 10))
    Traceback (most recent call last):
    ValueError: "center" must contain two integers, not ('a', 10)
    """
    if _is_indexable(arg):
        if _is_int(arg[0]) and _is_int(arg[1]):
            return True
        raise ValueError(f'"center" must contain two integers, not {arg}')
    raise TypeError(f'"center" must be an indexable type with two items, not {arg}')


def _is_indexable(arg: Any) -> bool:
    """
        arg     : the argument that should be tested
    return true if arg is or can be converted into an int

    >>> _is_indexable((10, 10))
    True

    >>> _is_indexable(10)
    False
    """
    try:
        return arg[0] and len(arg) == 2
    except TypeError:
        # object of type n is not subscriptable
        # object of type n has no method len()
        pass
    except IndexError:
        #  object of type n's index is out of range
        pass
    return False


def _is_int(arg: Any) -> bool:
    """
        arg     : the argument that should be tested
    return true if arg is or can be converted into an int

    >>> _is_int((10, 10))
    False

    >>> _is_int("10")
    True
    """
    try:
        int(arg)
        return True
    except TypeError:
        # int() argument must be a string, a bytes-like object or a number
        pass
    except ValueError:
        # invalid literal for int() with base n
        pass
    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
