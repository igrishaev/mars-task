

import sys


def make_world(x, y):
    return x, y, ()


def parse_input(source):
    pass


def make_robot(x, y, ori):
    return (x, y, ori)


def rotate_robot(robot, step):

    x, y, ori = robot

    rules = {
        ("N", "L"): "W",
        ("_", "_"): "_",
        ("_", "_"): "_",
        ("_", "_"): "_",
        ("_", "_"): "_",
        ("_", "_"): "_",
        ("_", "_"): "_",
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


def will_fall(world, robot):
    pass


def is_scent(world, robot):
    pass


def set_scent(world, robot):
    x, y, scents = world
    _x, _y, _ori = robot
    return x, y, scents + (_x, _y)


def update(world, robot, step):

    if step in "LR":
        return True, world, rotate_robot(robot, step)

    if step == "F":

        next_robot = move_robot(robot)

        if will_fall(world, next_robot):
            return False, set_scent(world, next_robot), robot

        if is_scent(world, next_robot):
            return True, world, robot

        return True, world, next_robot


def main():
    x, y, inputs = parse_input(sys.stdin)
    world = make_world(x, y)

    for (x, y, ori, steps) in inputs:
        robot = make_robot(x, y, ori)
        for step in steps:
            ok, world, robot = update(world, robot, step)
            if not ok:
                break
