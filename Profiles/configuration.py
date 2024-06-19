import pandas as pd

import numpy as np


def crear_perfil_base(hours, patrones):
    return pd.Series(patrones, index=pd.date_range("2024-01-01", periods=hours, freq="h"))

BASE_PROFILES1 = {
    'residencial_A': crear_perfil_base(24, [0.2, 0.2, 0.1, 0.1, 0.1, 0.3, 0.5, 0.8, 1.0, 1.2, 1.0, 0.8, 0.7, 0.6, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.0, 0.8, 0.5]),
    'residencial_B': crear_perfil_base(24, [0.4, 0.4, 0.3, 0.3, 0.3, 0.5, 0.7, 1.0, 1.5, 1.8, 1.5, 1.2, 1.0, 0.9, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.5, 1.2, 0.9, 0.6]),
    'comercio_pequeño': crear_perfil_base(24, [0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.6, 1.0, 1.4, 1.8, 1.5, 1.0, 0.8, 0.6, 0.5, 0.6, 0.8, 1.0, 1.2, 1.4, 1.2, 0.8, 0.6, 0.4]),
    'comercio_grande': crear_perfil_base(24, [0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.7, 1.2, 1.6, 2.0, 1.7, 1.4, 1.2, 1.0, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 1.6, 1.2, 1.0, 0.7]),
    'oficina_pequeña': crear_perfil_base(24, [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.5, 1.0, 1.5, 1.8, 1.5, 1.2, 1.0, 0.8, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.2, 0.8, 0.6, 0.4]),
    'oficina_grande': crear_perfil_base(24, [0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.6, 1.1, 1.7, 2.0, 1.8, 1.5, 1.2, 1.0, 0.8, 1.0, 1.2, 1.5, 1.7, 1.9, 1.5, 1.0, 0.8, 0.5]),
}

BASE_PROFILES1['residencial_A'].to_excel('output.xlsx')