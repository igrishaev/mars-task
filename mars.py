
import sys


def make_world(x, y):
    return x, y, ()


def parse_input(source):
    # line = source.readline()
    # x, y = map(int, line.split(" "))

    # routes = []
    # lines = source.readlines()
    # # routes = []
    # #
    # # for line in lines:
    # #     ln =
    # #     x, y, ori, steps
    # #     routes.append(x, y, ori, steps)
    # return x, y, routes
    return (10, 20, [
        (3, 19, "N", ("F", "F", "F")),
        (3, 19, "N", ("F", "F", "F")),
    ])


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
        ("S", "E"): "W",

        ("W", "L"): "S",
        ("W", "R"): "N",
    }

    new_ori = rules[(ori, step)]
    return x, y, new_ori


def move_robot(robot):
    x, y, ori = robot

    rules = {
        "N": (0, 1),
        "W": (1, 0),
        "S": (0, -1),
        "E": (-1, 0)

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

    results = []

    for (x, y, ori, steps) in routes:
        robot = make_robot(x, y, ori)
        for step in steps:
            ok, world, robot = update(world, robot, step)
            print ok, world, robot
            if not ok:
                break
        results.append(robot)

    return results



def main():
    x, y, routes = parse_input(sys.stdin)
    results = play(x, y, routes)
    print results


if __name__ == "__main__":
    main()
