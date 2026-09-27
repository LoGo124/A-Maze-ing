import sys
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class Config(BaseModel):
    """Clase que representa la configuración del laberinto usando Pydantic para validación de datos.

    Attributes:
        width (int): Ancho del laberinto.
        height (int): Altura del laberinto.
    """
    width: int = Field(..., gt=6, lt=80, description="Ancho del laberinto (debe ser un entero positivo entre 7 y 79).")
    height: int = Field(..., gt=6, lt=80, description="Altura del laberinto (debe ser un entero positivo entre 7 y 79).")
    entry: tuple[int, int] = Field(..., description="Coordenadas de entrada del laberinto (x, y).")
    exit: tuple[int, int] = Field(..., description="Coordenadas de salida del laberinto (x, y).")
    output_file: str = Field(..., description="Nombre del archivo de salida donde se guardará el laberinto generado.")
    perfect: bool = Field(..., description="Indica si el laberinto debe ser perfecto (sin bucles) o no.")
    seed: Optional[int] = Field(..., description="Semilla opcional para la generación del laberinto (si se proporciona, el laberinto será reproducible).")

    def _validate_coordinate(self, x: int, y: int) -> tuple[int, int]:
        x = min(x, self.width - 1) if x > 0 else 0
        y = min(y, self.height - 1) if y > 0 else 0
        return (x, y)


    @model_validator(mode='after')
    def validate_config(self):
        self.entry = self._validate_coordinate(*self.entry)
        self.exit = self._validate_coordinate(*self.exit)
        return self


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
                config_dict = {}
                for line in f:
                    key, value = line.strip().split("=")
                    config_dict[key.lower()] = value
                    if key in ["ENTRY", "EXIT"]:
                        x, y = map(int, value.split(","))
                        config_dict[key.lower()] = (x, y)
                conf = Config(**config_dict)
                return conf
        except OSError as e:
            sys.stderr.write(f"Error al abrir el archivo de configuración: {e}\n")
            raise
        except Exception as e:
            sys.stderr.write(f"Error al parsear la configuración: {e}\n")
            raise
