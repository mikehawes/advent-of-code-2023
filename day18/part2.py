from dataclasses import dataclass

from day18.instruction import DigInstruction


@dataclass
class Vertex:
    x: float
    y: float


def compute_lagoon_capacity(instructions: list[DigInstruction]):
    x = 0
    y = 0
    vertices = []
    for instruction in instructions:
        vertices.append(Vertex(x, y))
        x_distance, y_distance = split_instruction_distance(instruction)
        x += x_distance
        y += y_distance

    products_xy = 0
    products_yx = 0
    vertices = list(reversed(vertices))
    for i in range(0, len(vertices) - 1):
        products_xy += vertices[i].x * vertices[i + 1].y
        products_yx += vertices[i].y * vertices[i + 1].x
    area_inside_vertices = (products_yx - products_xy) / 2
    total_distance = sum(map(lambda i: i.distance, instructions))
    return area_inside_vertices + total_distance / 2 + 1


def split_instruction_distance(instruction: DigInstruction):
    x_distance = 0
    y_distance = 0
    distance = instruction.distance
    match instruction.direction:
        case 'L':
            x_distance = -distance
        case 'R':
            x_distance = distance
        case 'U':
            y_distance = -distance
        case 'D':
            y_distance = distance
    return x_distance, y_distance
