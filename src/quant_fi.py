import numpy as np
import pandas as pd
import time
import datetime as dt


def calcular_ema(df, columna='Precio', window=5, shift_n=0):
    """
    Calcula la EMA y la agrega al DF.

    Parámetros:
    df (pd.DataFrame): DataFrame con los datos de precios.
    columna (str): Nombre de la columna que contiene los precios.
    window (int): Ventana de suavizado para la EMA.
    shift_n (int): Cuántos períodos desplazar la EMA (positivo = mueve adelante).

    Return:
    pd.DataFrame: El DF con una nueva columna 'EMA_<window>'.
    """
    df = df.copy()
    
    alpha = 2 / (window + 1)  # Factor de suavizado
    precios = df[columna].values
    ema = [None] * len(precios)  # Lista para la EMA


    if len(precios) >= window:
        # Calculamos la SMA con los primeros 'window' valores
        ema[window - 1] = sum(precios[:window]) / window  

        # Aplicamos la fórmula recursiva de la EMA
        for t in range(window, len(precios)):
            ema[t] = alpha * precios[t] + (1 - alpha) * ema[t - 1]

    serie_ema = pd.Series(ema, index=df.index)

    # Adelantamos o retrasamos x velas
    if shift_n != 0:
        serie_ema = serie_ema.shift(shift_n)

    df[f'EMA_{window}'] = serie_ema
    # df[f'EMA_{window}'] = df[f'EMA_{window}'].fillna(0)
    return df


# guardo el codigo
def calcular_ema_backup(df, columna='Precio', window=5):
    """
    Calcula la EMA y la agrega al DF.

    Parámetros:
    df (pd.DataFrame): DataFrame con los datos de precios.
    columna (str): Nombre de la columna que contiene los precios.
    window (int): Ventana de suavizado para la EMA.

    Return:
    pd.DataFrame: El DF con una nueva columna 'EMA_<window>'.
    """
    df = df.copy()
    
    alpha = 2 / (window + 1)  # Factor de suavizado
    precios = df[columna].values
    ema = [None] * len(precios)  # Lista para la EMA

    # Calculamos la SMA con los primeros 'window' valores
    ema[window - 1] = sum(precios[:window]) / window  

    # Aplicamos la fórmula recursiva de la EMA
    for t in range(window, len(precios)):
        ema[t] = alpha * precios[t] + (1 - alpha) * ema[t - 1]

    df[f'EMA_{window}'] = ema
    df[f'EMA_{window}'] = df[f'EMA_{window}'].fillna(0)
    return df