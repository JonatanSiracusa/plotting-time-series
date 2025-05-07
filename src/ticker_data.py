import pandas as pd
from src.utils import insert_ohlc_cols, insert_ohlcav_cols, calc_returns_df, calc_returns_volat_df, calculate_returns, calc_prices_df, calculate_volat


class TickerData:
	def __init__(self, tickers, prices, tipo_precio=None):
		self.tickers = tickers
		self.prices = prices
		self.tipo_precio = tipo_precio

		tickers_added = ''
		for ticker in tickers:
			df = pd.DataFrame({}, index=prices.index)			
			df.fillna(0, inplace=True)
			df[df < 0] = 0
			setattr(self, ticker, df)	# asignamos el DF como atributo de la Class
			tickers_added += ticker + ', '
		
		print(f'Se agregaron a la Class los DataFrame de {tickers_added.rstrip(", ")}.')


	def list_tickers(self):
		""" Vemos los DF creados, correspondientes a cada ticker """
		return self.tickers


	def load_ohlc(self):
		""" La Function externa inserta columnas de precio OHLC para graficar en cada DF VACIO de la clase. """
		insert_ohlc_cols(self)


	def load_ohlcav(self):
		""" La Function externa inserta columnas de precio OHLCAV en cada DF VACIO de la clase. """
		insert_ohlcav_cols(self)	


	def add_columns(self, function, **kwargs):
		"""
		Agregamos columnas a todos los DF de la Class llamando a una Function externa.

		Parámetros:
		- function: la function externa que recibe un DF y devuelve un DF modificado con nuevas cols o calculos.
		- kwargs: parámetros adicionales que pueda necesitar la function externa.

		Ejemplo de uso: data.add_columns(calculate_ema, EMA1=10, EMA2=20)
		"""
		for ticker in self.tickers:
			df = getattr(self, ticker)
			df, msg = function(df, **kwargs)
			setattr(self, ticker, df)
		
		print(f'Agregados a los DF de la Class usando "{function.__name__}": {msg}.')
		

	def create_prices_df(self, column_price='Close'):
		self.prices_df = calc_prices_df(self, column_price=column_price)
		return self.prices_df
		

	def create_returns_df(self, method='log', column_price='Adj Close'):
		self.returns_df = calc_returns_df(self, method=method, column_price=column_price)
		return self.returns_df
	

	def create_returns_volat_df(self, method='log', column_price='Adj Close', window=40): 
		self.returns_volat_df = calc_returns_volat_df(self, method=method, column_price=column_price, window=window)
		return self.returns_volat_df
	

	def backup_dataframes(self, suffix='_v1'):
		df_added = []
		for ticker in self.tickers:
			df = getattr(self, ticker)
			df_copy = df.copy(deep=True)
			setattr(self, f'{ticker}{suffix}', df_copy)
			df_added.append(f'{ticker}{suffix}')
		print(f'Se crearon copias INTERNAS de la INSTANCIA de los DF:\n{", ".join(df_added)}.\n')


	def backup_dataframes_to_globals(self, suffix='_v1'):
		df_added = []
		for ticker in self.tickers:
			df = getattr(self, ticker)
			df_copy = df.copy(deep=True)
			globals()[f'{ticker}{suffix}'] = df_copy
			# setattr(self, f'{ticker}{suffix}', df_copy)
			df_added.append(f'{ticker}{suffix}')
		print(f'Se crearon copias GLOBALES de los DF:\n{", ".join(df_added)}.\n')




def export_selected_dataframes(self, tickers=None, suffix='_v1', folder='exports'):
    """
    Exporta los DataFrames seleccionados a archivos CSV.

    - tickers: lista de tickers a exportar (si None, usa todos).
    - suffix: sufijo del atributo a exportar, como '_v1' para las copias.
    - folder: carpeta destino.
    """
    os.makedirs(folder, exist_ok=True)
    tickers = tickers or self.tickers
    exportados = []

    for ticker in tickers:
        attr_name = f"{ticker}{suffix}"
        if hasattr(self, attr_name):
            df = getattr(self, attr_name)
            if isinstance(df, pd.DataFrame):
                filepath = os.path.join(folder, f"{attr_name}.csv")
                df.to_csv(filepath)
                exportados.append(attr_name)
    
    print(f"[CSV] Exportados {len(exportados)} archivos a carpeta '{folder}': {', '.join(exportados)}.")


import os

def export_dataframes_to_csv(self, folder='exports', include_suffix='_v1', only_suffix=True):
    """
    Exporta los DataFrames de la instancia a archivos CSV.

    Parámetros:
    - folder: carpeta donde se guardan los archivos CSV.
    - include_suffix: si se especifica, solo se exportan DataFrames con ese sufijo en el nombre.
    - only_suffix: si True, exporta solo los que terminan con el sufijo. Si False, exporta todos.
    """
    os.makedirs(folder, exist_ok=True)
    exportados = []

    for attr_name in dir(self):
        if only_suffix and not attr_name.endswith(include_suffix):
            continue
        attr = getattr(self, attr_name)
        if isinstance(attr, pd.DataFrame):
            filepath = os.path.join(folder, f"{attr_name}.csv")
            attr.to_csv(filepath)
            exportados.append(attr_name)
    
    print(f"[CSV] Exportados a carpeta '{folder}': {', '.join(exportados)}.")


