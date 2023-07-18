import aiohttp
import asyncio


async def get_text_matrix(url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    except aiohttp.ClientError as e:
        print(f"ClientError: {e}")
    except asyncio.TimeoutError:
        print("Connection Timeout")
    except ConnectionRefusedError as e:
        print(f"ConnectionRefusedError: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


def change_direction(x_dir: int, y_dir: int) -> tuple[int, int]:
    # from downside to right
    if y_dir == 1:
        y_dir = 0
        x_dir = 1
    # from right to upside
    elif x_dir == 1:
        x_dir = 0
        y_dir = -1
    # from upside to left
    elif y_dir == -1:
        y_dir = 0
        x_dir = -1
    # from left to downside
    elif x_dir == -1:
        x_dir = 0
        y_dir = 1
    return x_dir, y_dir


def is_quadratic(matrix_list: list[list[int]]) -> bool:
    matrix_len = len(matrix_list)
    for row in matrix_list:
        if len(row) != matrix_len:
            return False
    return True


def prepare_matrix(text: str) -> list[list[int]]:
    matrix_list = []
    row = []
    str_num = ''
    for char in text:
        if char.isdigit():
            str_num = str_num + char
        elif len(str_num) and char != '\n':
            row.append(int(str_num))
            str_num = ''
        elif len(row) and char == '\n':
            matrix_list.append(row)
            row = []
    # check if matrix is not empty and if it's quadratic
    if matrix_list and is_quadratic(matrix_list):
        return matrix_list
    return []


def traverse_matrix(quad_matrix: list[list[int]]) -> list[int]:
    result = []
    x = 0
    y = -1     # -1 for lookup check in the 1st if in a while loop
    x_dir = 0  # -1 0 1
    y_dir = 1  # -1 0 1 (first move direction : downside)
    size = len(quad_matrix)
    max_moves_count = size ** 2
    move_counter = 0
    while move_counter < max_moves_count:
        # check not to go beyond x,y boundaries and not to visited cells
        next_x_pos = x + x_dir
        next_y_pos = y + y_dir
        if (0 <= next_x_pos < size) and (0 <= next_y_pos < size) and \
                (quad_matrix[next_y_pos][next_x_pos]):
            x = next_x_pos
            y = next_y_pos
            result.append(quad_matrix[y][x])
            quad_matrix[y][x] = False
            move_counter += 1
        else:
            x_dir, y_dir = change_direction(x_dir, y_dir)

    return result


async def get_matrix(url: str) -> list[int]:
    initial_matrix = prepare_matrix(await get_text_matrix(url))
    result_list = traverse_matrix(initial_matrix)
    return result_list
