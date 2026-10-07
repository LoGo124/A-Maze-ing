"""Module for parsing and validating maze configuration files"""

import sys

from typing import Tuple, Dict, List

from pydantic import BaseModel, Field, ValidationError


VALID_CONFIG_KEYS: List[str] = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
    "SEED",
]


class ConfigSyntaxError(Exception):
    """Custom exception raised when config.txt has invalid syntax."""
    def __init__(self, message: str = "") -> None:
        valid_configs = VALID_CONFIG_KEYS
        base_msg = (
            "Valid config.txt syntax: key=value\n"
            f"Valid keys: {valid_configs}"
        )
        full_message = f"{message}\n{base_msg}" if message else base_msg
        super().__init__(full_message)


class Config(BaseModel):
    """Class that represents the maze configuration using Pydantic
    for data validation.

    Attributes:
        width (int): Width of the maze.
        height (int): Height of the maze.
        entry: The 0-indexed (x, y) coordinates of the entry point.
        exit_point: The 0-indexed (x, y) coordinates of the exit point.
        output_file: The path to the output file where the maze will be saved.
        perfect: Whether the maze must be perfect (spanning tree) or looping.
    """

    width: int = Field(..., gt=2, le=80)
    height: int = Field(..., gt=2, le=80)
    entry: Tuple[int, int] = Field(...)
    exit: Tuple[int, int] = Field(...)
    output_file: str = Field(...)
    perfect: bool = Field(...)
    seed: int | None = None


class ConfigParser:
    """Class responsible for parsing and validating the maze configuration.

    Attributes:
        config (Config): An instance of the Config class containing the
            validated configuration..
    """

    @staticmethod
    def load_config(path: str) -> Config:
        """Load and validate the maze configuration from a file.

        Args:
            path (str): Path to the configuration file.

        Returns:
            Config: An instance of the Config class.
        """
        raw_data: Dict[str, str] = {}
        try:
            with open(path, "r", encoding="utf-8") as file:
                for raw_line in file:
                    line = raw_line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        raise ConfigSyntaxError(f"Invalid line format: {line}")
                    key_text, value = line.split("=", 1)
                    key = key_text.strip().upper()
                    value = value.strip()
                    if key not in VALID_CONFIG_KEYS:
                        raise ConfigSyntaxError(
                            f"Caught invalid configuration key error: {key}"
                        )
                    if not key or not value:
                        raise ConfigSyntaxError(
                            f"{key}'s value cannot be empty."
                        )
                    if key in raw_data:
                        raise ConfigSyntaxError(
                            f"Duplicate key found: {key}"
                        )
                    raw_data[key] = value
        except PermissionError as e:
            sys.exit(f"\nPermission denied when opening file: {e}\n")
        except OSError as e:
            sys.exit(f"\nError opening the configuration file: {e}\n")
        except ConfigSyntaxError as e:
            sys.exit(f"\nError parsing configuration: {e}\n")

        try:
            # Mandatory keys check
            mandatory: List[str] = ["WIDTH",
                                    "HEIGHT",
                                    "ENTRY",
                                    "EXIT",
                                    "OUTPUT_FILE",
                                    "PERFECT"]
            for key in mandatory:
                if key not in raw_data:
                    raise ConfigSyntaxError(f"Missing mandatory key: {key}")

            # Data type conversion and validation
            # Config construction will validate the Config class
            entry = ConfigParser._parse_coordinates(raw_data["ENTRY"])
            exit_coord = ConfigParser._parse_coordinates(raw_data["EXIT"])

            width = int(raw_data["WIDTH"])
            height = int(raw_data["HEIGHT"])
            if raw_data["PERFECT"].lower() == "true":
                perfect = True
            elif raw_data["PERFECT"].lower() == "false":
                perfect = False
            else:
                raise ConfigSyntaxError(
                    "PERFECT must be True or False."
                )
            seed_value: int | None = None
            if "SEED" in raw_data:
                seed_value = int(raw_data["SEED"])

            return Config(
                        width=width,
                        height=height,
                        entry=entry,
                        exit=exit_coord,
                        output_file=raw_data["OUTPUT_FILE"],
                        perfect=perfect,
                        seed=seed_value,
                    )

        except ValidationError as e:
            sys.exit(f"\nPydantic validation error: {e}\n")
        except ConfigSyntaxError as e:
            sys.exit(f"\nError parsing configuration: {e}\n")
        except ValueError as e:
            sys.exit(f"\nInvalid value in configuration: {e}\n")
        except Exception as e:
            sys.exit(f"\nError parsing configuration: {e}\n")

    @staticmethod
    def _parse_coordinates(value: str) -> tuple[int, int]:
        """Convert 'x,y' into a tuple of two integers."""

        coords = value.split(",")
        if len(coords) != 2:
            raise ConfigSyntaxError(
                f"Invalid coordinates: {value}"
            )
        try:
            x = int(coords[0].strip())
            y = int(coords[1].strip())
            return (x, y)
        except ValueError as e:
            sys.stderr.write(f"\nInvalid coordinates: {value} Usage: x,y")
            sys.exit(f"\nError parsing configuration: {e}\n")
