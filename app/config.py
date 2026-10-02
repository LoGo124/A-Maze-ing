import sys
from typing import Optional
from pydantic import BaseModel, ValidationError, Field


class ConfigSyntaxError(ValidationError):
    def __init__(self, *args):
        valid_configs = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"]
        super().__init__(f"Valid config.txt syntax: key=value\nValid keys: {valid_configs}", *args)


class Config(BaseModel):
    """Clase que representa la configuración del laberinto usando Pydantic para validación de datos.

    Attributes:
        width (int): Ancho del laberinto.
        height (int): Altura del laberinto.
    """
    width: int = Field(..., gt=2, lt=80, description="Ancho del laberinto (debe ser un entero positivo entre 7 y 79).")
    height: int = Field(..., gt=2, lt=80, description="Altura del laberinto (debe ser un entero positivo entre 7 y 79).")
    entry: tuple[int, int] = Field(..., description="Coordenadas de entrada del laberinto (x, y).")
    exit: tuple[int, int] = Field(..., description="Coordenadas de salida del laberinto (x, y).")
    output_file: str = Field(..., description="Nombre del archivo de salida donde se guardará el laberinto generado.")
    perfect: Optional[bool] = Field(..., description="Indica si el laberinto debe ser perfecto (sin bucles) o no.")
    seed: Optional[int] = None


class ConfigParser:
    """Clase que se encarga de parsear y validar la configuración del laberinto.

    Attributes:
        config (Config): Instancia de la clase Config que contiene la configuración validada.
    """
    def load_config(path: str) -> Config:
        """Carga y valida la configuración del laberinto a partir de un archivo.

        Args:
            path (str): Ruta al archivo de configuración.

        Returns:
            Config: Instancia de la clase Config con la configuración validada.
        """
        try:
            with open(path, "r") as f:
                valid_configs = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"]
                config_dict = {}
                for line in f:
                    if line[0] == "#":
                        continue
                    elif not ("=" in line):
                        raise ConfigSyntaxError()
                    key, value = line.strip().split("=")
                    if key.upper() in valid_configs:
                        config_dict[key.lower()] = value
                        if key in ["ENTRY", "EXIT"]:
                            x, y = map(int, value.split(","))
                            config_dict[key.lower()] = (x, y)
                    else:
                        raise ConfigSyntaxError()
                conf = Config(**config_dict)
                return conf
        except OSError as e:
            sys.stderr.write(f"Error al abrir el archivo de configuración: \n{e}\n")
        except ConfigSyntaxError as e:
            sys.stderr.write(f"Error al parsear la configuración: \n{e}\n")
        except ValidationError as e:
            sys.stderr.write(f"Pydantic validation error: \n{e}\n")
        except Exception as e:
            sys.stderr.write(f"Unknown error: \n{e}\n")
