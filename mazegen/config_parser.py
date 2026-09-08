from typing import Optional
from pydantic import BaseModel, PositiveInt, Field


class Config(BaseModel):
    """Clase que representa la configuración del laberinto usando Pydantic para validación de datos.

    Attributes:
        width (int): Ancho del laberinto.
        height (int): Altura del laberinto.
    """
    width: PositiveInt = Field(..., gt=6, lt=80, description="Ancho del laberinto (debe ser un entero positivo entre 7 y 79).")
    height: PositiveInt = Field(..., gt=6, lt=80, description="Altura del laberinto (debe ser un entero positivo entre 7 y 79).")
    entry: tuple[int, int] = Field(..., description="Coordenadas de entrada del laberinto (x, y).")
    exit: tuple[int, int] = Field(..., description="Coordenadas de salida del laberinto (x, y).")
    output_file: str = Field(..., description="Nombre del archivo de salida donde se guardará el laberinto generado.")
    perfect: bool = Field(..., description="Indica si el laberinto debe ser perfecto (sin bucles) o no.")
    seed: Optional[int] = Field(..., description="Semilla opcional para la generación del laberinto (si se proporciona, el laberinto será reproducible).")


class ConfigParser:
    """Clase que se encarga de parsear y validar la configuración del laberinto.

    Attributes:
        config (Config): Instancia de la clase Config que contiene la configuración validada.
    """
    def load_config(self, path: str) -> Config:
        """Carga y valida la configuración del laberinto a partir de un archivo.

        Args:
            path (str): Ruta al archivo de configuración.

        Returns:
            Config: Instancia de la clase Config con la configuración validada.
        """
        with open(path, "r") as f:
            config_data = yaml.safe_load(f)
        return Config(**config_data)
