
import sys
from StringIO import StringIO


def make_world(w, h):
    """
    The world is represented by a tuple (w, h, scents), where:
    - w: width,
    - h: height,
    - scents: a tuple of pairs (x, y).
    """
    return w, h, ()


def parse_input(source):
    """
    Parses input data from a file-like object.
    Returns a tuple (w, h, routes), where:
    - w: width,
    - h: height,
    - routes: a tuple of (x, y, ori, steps), where:
    - x: x position,
    - y: y position,
    - ori: orientation, eg N, E, S, W
    - steps: a string of robot commands, eg FLRFLF
    """

    lines = source.readlines()
    lines = map(str.strip, lines)
    lines = filter(None, lines)

    head, rest = lines[0], lines[1:]

    w, h = map(int, head.split(" "))

    def parse_iter(lines, result=()):

        if not lines:
            return result

        line1 = lines[0]
        line2 = lines[1]

        x_str, y_str, ori = line1.split(" ")
        x = int(x_str)
        y = int(y_str)

        steps = line2
        node = (x, y, ori, steps)

        return parse_iter(lines[2:], result + (node, ))

    routes = parse_iter(rest)
    return w, h, routes


def compose_results(results):
    """
    Turns game results into a string.
    """
    def process(node):
        ok, (x, y, ori) = node
        return ('%s %s %s %s' % (
            x, y, ori, ("" if ok else "LOST")
        )).strip()


    return '\n'.join(map(process, results))


def make_robot(x, y, ori):
    """
    Makes a robot data structure.
    """
    return (x, y, ori)


def rotate_robot(robot, step):
    """
    Returns a new rotated robot.
    """
    x, y, ori = robot

    rules = {
        ("N", "L"): "W",
        ("N", "R"): "E",

        ("E", "L"): "N",
        ("E", "R"): "S",

        ("S", "L"): "E",
        ("S", "R"): "W",

        ("W", "L"): "S",
        ("W", "R"): "N",
    }

    new_ori = rules[(ori, step)]
    return x, y, new_ori


def move_robot(robot):
    """
    Returns a new moved robot.
    """
    x, y, ori = robot

    rules = {
        "N": (0, 1),
        "W": (-1, 0),
        "S": (0, -1),
        "E": (1, 0),
    }

    dx, dy = rules[ori]

    return (
        x + dx,
        y + dy,
        ori,
    )


def is_placed(world, robot):
    """
    Checks whether a robot fits the world.
    """
    w, h, _ = world
    x, y, _ = robot

    return (
        0 <= x <= w
        and 0 <= y <= h
    )


def is_scent(world, robot):
    """
    Checks whether a robot stands on a scent cell.
    """
    _, _, scents = world
    x, y, _ = robot

    return (x, y) in scents


def set_scent(world, robot):
    """
    Marks a cell that robot stands on as scent.
    Returns a new world.
    """
    w, h, scents = world
    x, y, _ = robot
    return w, h, scents + ((x, y), )


def update(world, robot, step):
    """
    Makes a game turn. Returns a tuple (ok, world, robot), where:
    - world: a new world;
    - robot: a new robot;
    - ok: whether a robot is on board or not (has fallen).
    """
    if step in "LR":
        return world, rotate_robot(robot, step), True

    if step == "F":

        robot_next = move_robot(robot)
        placed_next = is_placed(world, robot_next)

        if is_scent(world, robot):
            if placed_next:
                return world, robot_next, True
            else:
                return world, robot, True

        else:
            if placed_next:
                return world, robot_next, True
            else:
                return set_scent(world, robot), robot, False


def robot_play(world, robot, steps):

    def iterate(world, robot, steps, flag):
        if steps and flag:
            world, robot, flag = update(world, robot, steps[0])
            return iterate(world, robot, steps[1:], flag)
        else:
            return world, robot, flag

    return iterate(world, robot, steps, True)


def play(w, h, routes):
    """
    Plays the game. Returns a tuple of (ok, robot), where:
    - ok: whether a robot has reached the target (didn't fall);
    - robot: a final robot's state.
    """
    world = make_world(w, h)
    results = ()

    for (x, y, ori, steps) in routes:
        robot = make_robot(x, y, ori)
        world, robot, flag = robot_play(world, robot, steps)
        results += ((flag, robot), )

    return results


def main():
    w, h, routes = parse_input(sys.stdin)
    results = play(w, h, routes)
    print compose_results(results)


# ---- tests


def assert_eq(v1, v2):
    try:
        assert v1 == v2
    except AssertionError as e:
        print v1, " == ", v2
        raise e


def test_rotate():
    assert_eq(make_robot(0, 0, "E"),
              rotate_robot(make_robot(0, 0, "N"), "R"))

    assert_eq(make_robot(0, 0, "W"),
              rotate_robot(make_robot(0, 0, "N"), "L"))


def test_move_simple():
    res = play(10, 20, (
        (0, 0, "N", "FRF"),
    ))
    assert_eq(res, ((True, (1, 1, 'E')),))


def test_rotate_simple():
    res = play(10, 20, (
        (0, 0, "N", "L"),
    ))
    assert_eq(res, ((True, (0, 0, 'W')),))


def test_rotate_full():
    res = play(10, 20, (
        (0, 0, "N", "LLLL"),
    ))
    assert_eq(res, ((True, (0, 0, 'N')),))


def test_go_circle():
    res = play(10, 20, (
        (5, 5, "N", "RRFLFLFLFR"),
    ))
    assert_eq(res, ((True, (5, 5, 'N')),))


def test_drops():
    res = play(10, 20, (
        (5, 5, "N", "FFFFFFFFFFFFFFFF"),
    ))
    assert_eq(res, ((False, (5, 20, 'N')),))


def test_scent():
    res = play(10, 20, (
        (5, 5, "N", "FFFFFFFFFFFFFFFF"),
        (5, 5, "N", "FFFFFFFFFFFFFFFF"),
    ))
    assert_eq(res, (
        (False, (5, 20, 'N')),
        (True, (5, 20, 'N')),
    ))


def test_scent_more():
    res = play(10, 20, (
        (5, 5, "N", "FFFFFFFFFFFFFFFF"),
        (5, 5, "N", "FFFFFFFFFFFFFFFFRF"),
    ))
    assert_eq(res, (
        (False, (5, 20, 'N')),
        (True, (6, 20, 'E')),
    ))


def test_composer():
    output = compose_results((
        (True, (1, 2, "N")),
        (False, (5, 20, "L")),
        (True, (8, 42, "S")),
    ))
    assert_eq(output, "1 2 N\n5 20 L LOST\n8 42 S")


def test_parser():
    io = StringIO()
    io.write('3 5\n')
    io.write('1 2 N\n')
    io.write('FFLFRL\n')
    io.write('\n')
    io.write('20 1 S\n')
    io.write('LLRRFFL\n')
    io.seek(0)

    data = parse_input(io)
    assert_eq(data, (3, 5, (
        (1, 2, "N", "FFLFRL"),
        (20, 1, "S", "LLRRFFL"),
    )))


def run_tests():
    """
    Naive test runner.
    """
    for (name, func) in globals().iteritems():
        if name.startswith("test_"):
            func()


if __name__ == "__main__":
    if "test" in sys.argv:
        run_tests()
    else:
        main()
