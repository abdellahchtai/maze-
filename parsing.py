from typing import Dict

def check_width(value: str) -> str | bool:
    """Validate the WIDTH value from the configuration file.

    Args:
        value (str): The width value as a string.

    Returns:
        bool: True if the width is a valid integer bigger than 2.
        str: Error message if the value is not an integer or out of range.
    """
    try:
        width = int(value)
        if  width < 2:
            return "WIDTH must bigger than 2"
        return True
    except ValueError:
        return "WIDTH must be an integer"


def check_height(value: str) -> str | bool:
    """Validate the HEIGHT value from the configuration file.

    Args:
        value (str): The height value as a string.

    Returns:
        bool: True if the height is a valid integer bigger than 2.
        str: Error message if the value is not an integer or out of range.
    """
    try:
        height = int(value)
        if height < 2:
            return "HEIGHT must bigger than 2"
        return True
    except ValueError:
        return "HEIGHT be an integer"


def check_entry(value: str) -> str | bool:
    """
    Validate the ENTRY coordinate value from the configuration file.

    Args:
        value (str): The string value of the ENTRY key, expected in the format "x,y".

    Returns:
        bool | str: Returns True if the value is valid.
                     Returns an error message string if:
                     - The format is incorrect (not "x,y").
                     - Either coordinate is empty.
                     - Either coordinate is not an integer.
    """
    try:
        entry_array = value.split(",")
        if len(entry_array) != 2:
            return "Invalid format, format example: ENTRY=(10,10)"
        str_x, str_y = entry_array
        if not str_x or not str_y:
            return "coordinates should not be empty, format example: ENTRY=(0,0)"
        _ = int(str_x)
        _ = int(str_y)
        return True
    except ValueError:
        return "coordinates must be a valid integer"


def valid_coord_range(entry_value: str, exit_value: str, width: str, height: str) -> str | bool:
    """Validate that ENTRY and EXIT coordinates are within maze bounds and not the same.

    Args:
        entry_value (str): Entry coordinates as "x,y".
        exit_value (str): Exit coordinates as "x,y".
        width (str): Maze width as a string.
        height (str): Maze height as a string.

    Returns:
        bool: True if coordinates are valid.
        str: Error message if coordinates are invalid, out of bounds, or identical.
    """
    try:
        entry_coord = entry_value.split(",")
        exit_coord = exit_value.split(",")
        str_entry_x, str_entry_y = entry_coord
        str_exit_x, str_exit_y = exit_coord
        if not str_entry_x or not str_entry_y or not str_exit_x or not str_exit_y:
            return "coordinats should not be empty, format example: ENTRY=0,0"
        entry_x = int(str_entry_x)
        entry_y = int(str_entry_y)
        exit_x = int(str_exit_x)
        exit_y = int(str_exit_y)
        wid = int(width)
        heig = int(height)
        if entry_x < 0 or entry_x > wid - 1 or exit_x < 0 or exit_x > wid - 1:
            return f"ENTRY/EXIT x coordinate out of bounds (0–{wid - 1})"
        if entry_y < 0 or entry_y > heig - 1 or exit_y < 0 or exit_y > heig - 1:
            return f"ENTRY/EXIT y coordinate out of bounds (0–{heig - 1})"
        if entry_x == exit_x and entry_y == exit_y:
            return "Entry and Exit must be different"
        return True
    except ValueError:
        return "must be an integer"


def check_exit(value: str) -> str | bool:
    """Validate the EXIT coordinates from the configuration file.

    Args:
        value (str): Exit coordinates as "x,y".

    Returns:
        bool: True if the exit coordinates are valid.
        str: Error message if the format is invalid or coordinates are not integers.
    """
    try:
        exit_array = value.split(",")
        if len(exit_array) != 2:
            return "Invalid format, format example: EXIT=10,10"
        str_x, str_y = exit_array
        if not str_x or not str_y:
            return "coordinats should not be empty, format example: EXIT=10,10"
        _ = int(str_x)
        _ = int(str_y)
        return True
    except ValueError:
        return "coordinates must be a valid integer"



def check_output_file(value: str) -> str | bool:
    """Validate the OUTPUT_FILE value from the configuration file.

    Args:
        value (str): Output file name as a string.

    Returns:
        bool: True if the output file is valid.
        str: Error message if the value is empty or does not end with '.txt'.
    """
    if not value:
        return "empty"
    if not value.endswith(".txt"):
        return "Invalid format for output file"
    return True


def check_perfect(value: str) -> str | bool:
    """Validate the PERFECT flag from the configuration file.

    Args:
        value (str): PERFECT value as a string (e.g., 'true', '1', 'yes', 'false', '0', 'no').

    Returns:
        bool: True if the value is valid.
        str: Error message if the value is not one of the allowed options.
    """
    val = value.strip(" \t").lower()
    if val in {"true", "1", "yes", "false", "0", "no"}:
        return True
    return "PERFECT must be true/false, 1/0, yes/no"


def parse_coordinates(value: str) -> tuple[int, int]:
    """Convert 'x,y' into (x, y) as integers."""
    x_str, y_str = value.split(",")
    return int(x_str), int(y_str)



def parse_config(file_name: str) -> Dict | str: 
    """
    Main execution block for reading and validating the maze configuration file.

    Reads 'config.txt', parses key-value pairs, checks for required keys, validates
    their values using corresponding validation functions, and ensures coordinates
    are within the valid maze range. Prints any errors encountered.
    """
    try:
        with open(file_name, "r") as file:
            # Mapping of required keys to their validation functions
            required_keys = {
                "WIDTH": check_width,
                "HEIGHT": check_height,
                "ENTRY": check_entry,
                "EXIT": check_exit,
                "OUTPUT_FILE": check_output_file,
                "PERFECT": check_perfect,
            }
            items = {}
            for line_number, line in enumerate(file, start=1):
                striped_line = line.strip()
                if striped_line == "":
                    continue
                elif striped_line.startswith("#"):
                    continue
                else:
                    array = striped_line.split("=")
                    if len(array) != 2:
                        raise ValueError(f"invalid format at line {line_number}")
                    key, value = array
                    if not key:
                        raise ValueError(f"empty key at line {line_number}")
                    if not value:
                        raise ValueError(
                            f"empty value for key ({key}) at line {line_number}"
                        )
                    if key in items:
                        raise ValueError(f"duplicate key ({key}) at line {line_number}")
                    key_striped = key.strip()
                    if key_striped in required_keys:
                        items[key_striped] = value.strip()
                    else:
                        raise ValueError(f"Invalid key value :{key_striped}")

            # Validate each key's value using its validation function
            for key, value in items.items():
                validation_result = required_keys[key](value)
                if isinstance(validation_result, str):
                    raise ValueError(validation_result)

            # Ensure all required keys exist
            key_list = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
            for key in key_list:
                if key not in items:
                    raise ValueError(f"({key}) does not exist in {file_name}")

            # Validate coordinates are within maze bounds
            valid_coordinates = valid_coord_range(
                items["ENTRY"], items["EXIT"], items["WIDTH"], items["HEIGHT"]
            )
            if isinstance(valid_coordinates, str):
                raise ValueError(valid_coordinates)

            items["WIDTH"] = int(items["WIDTH"])
            items["HEIGHT"] = int(items["HEIGHT"])
            items["ENTRY"] = parse_coordinates(items["ENTRY"])
            items["EXIT"] = parse_coordinates(items["EXIT"])
            items["PERFECT"] = items["PERFECT"].lower() in {"true", "1", "yes"}
            # for key, value in items.items():
            #     print(f"|{key}:{value}|")

            from maze_generator import MazeGenerator
            entry_coord = items["ENTRY"]
            exit_coord = items["EXIT"]
            maze = MazeGenerator(items["WIDTH"] , items["HEIGHT"],  entry_coord, exit_coord)
            maze.generate_maze("b")
            grid = maze.grid
            # for row_index, row in enumerate(grid):
            #     for col_index, cell in enumerate(row):
            #         current_coord = (row_index, col_index)
            #         if current_coord == entry_coord or current_coord == exit_coord:
            #             if cell.path_42 == True:
            if maze.grid[entry_coord[1]][entry_coord[0]].path_42 and maze.grid[exit_coord[1]][exit_coord[0]].path_42:
                raise ValueError("The ENTRY and EXIT coordinate must not be in the 42 draw")
            if maze.grid[entry_coord[1]][entry_coord[0]].path_42:
                raise ValueError("The ENTRY coordinate must not be in the 42 draw")
            if maze.grid[exit_coord[1]][exit_coord[0]].path_42:
                raise ValueError("The EXIT coordinate must not be in the 42 draw")
            

            return items
    except (FileNotFoundError, PermissionError, ValueError) as e:
        return e
