
import sys


def make_world(x, y):
    return x, y, ()


def parse_input(source):
    # line = source.readline()
    # x, y = map(int, line.split(" "))
    # todo
    # routes = []
    # lines = source.readlines()
    # # routes = []
    # #
    # # for line in lines:
    # #     ln =
    # #     x, y, ori, steps
    # #     routes.append(x, y, ori, steps)
    # return x, y, routes
    pass


def compose_results(results):
    # todo
    return ""


def make_robot(x, y, ori):
    return (x, y, ori)


def rotate_robot(robot, step):

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


def will_stand(world, robot):
    wx, wy, _ = world
    rx, ry, _ = robot

    return (
        0 <= rx <= wx
        and 0 <= ry <= wy
    )


def is_scent(world, robot):
    _, _, scents = world
    rx, ry, _ = robot

    return (rx, ry) in scents


def set_scent(world, robot):
    wx, wy, scents = world
    rx, ry, _ = robot
    return wx, wy, scents + ((rx, ry), )


def update(world, robot, step):

    if step in "LR":
        return True, world, rotate_robot(robot, step)

    if step == "F":

        next_robot = move_robot(robot)

        if not will_stand(world, next_robot):
            return False, set_scent(world, robot), robot

        if is_scent(world, next_robot):
            return True, world, robot

        return True, world, next_robot


def play(x, y, routes):
    world = make_world(x, y)

    results = ()

    for (x, y, ori, steps) in routes:
        robot = make_robot(x, y, ori)
        for step in steps:
            ok, world, robot = update(world, robot, step)
            if not ok:
                break

        results += ((ok, robot), )

    return results


def main():
    x, y, routes = parse_input(sys.stdin)
    results = play(x, y, routes)
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
    assert_eq(res, ((True, (0, 0, 'W')), ))


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
        (True, (5, 19, 'N')),
    ))


def test_scent_more():
    res = play(10, 20, (
        (5, 5, "N", "FFFFFFFFFFFFFFFF"),
        (5, 5, "N", "FFFFFFFFFFFFFFFFRF"),
    ))
    assert_eq(res, (
        (False, (5, 20, 'N')),
        (True, (6, 19, 'E')),
    ))



def main_tests():
    for (name, func) in globals().iteritems():
        if name.startswith("test_"):
            func()


if __name__ == "__main__":
    main_tests()
    # main()
