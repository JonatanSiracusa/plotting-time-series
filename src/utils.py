import numpy as np
import pandas as pd
import time
import datetime as dt
import yfinance as yf
from IPython.display import display, HTML, Javascript
import plotly.graph_objects as go
from IPython.display import Image, display

import base64
import plotly.io as pio


def get_data(df, categoria, ticker):
	return df.loc[:, (categoria, ticker)]


text_custom = f"""
"""
print(text_custom.lstrip())


def descargar_datos_yf(tickers, start_date=None, end_date=None, delay=1):
	if start_date is None:
		start_date = dt.datetime(2015, 1, 1)
	if end_date is None:
		end_date = dt.datetime.now()

	data_dict = {}
	for ticker in tickers:
		try:
			df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, progress=False)
			if not df.empty:
				data_dict[ticker] = df
				print(f'Descargado: {ticker}')
			else:
				print(f'Sin datos: {ticker}')
		except Exception as e:
			print(f'Error descargando {ticker}: {e}')
		time.sleep(delay)
	
	if data_dict:
		df = pd.concat(data_dict, axis=1)
	else:
		df = pd.DataFrame()

	return df


def insert_ohlc_cols(instancia):
	"""
	Inserta las columnas de precio OHLCAV a cada DataFrame vacio dentro de la clase TickerData.
	"""
	tickers_added = ''
	for ticker in instancia.tickers:
		df = getattr(instancia, ticker)
		try:
			df['Open'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[4])].squeeze()
			df['High'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[2])].squeeze()
			df['Low'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[3])].squeeze()
			df['Close'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[1])].squeeze()
			# df['Adj Close'] = instancia.prices.loc[:, (ticker, tipo_precio[0])].squeeze()
			# df['Volume'] = instancia.prices.loc[:, (ticker, tipo_precio[5])].squeeze()
			df.fillna(0, inplace=True)
			df[df < 0] = 0
			tickers_added += ticker + ', '
		except KeyError as e:
			print(f'Error al agregar precios para {ticker}: {e}')

	print(f'Se insertaron las columnas OHLCAV en los DF {tickers_added.rstrip(", ")}.')


def insert_ohlcav_cols(instancia):
	"""
	Inserta las columnas de precio OHLCAV a cada DataFrame vacio dentro de la clase TickerData.
	"""
	tickers_added = ''
	for ticker in instancia.tickers:
		df = getattr(instancia, ticker)
		try:
			df['Open'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[4])].squeeze()
			df['High'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[2])].squeeze()
			df['Low'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[3])].squeeze()
			df['Close'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[1])].squeeze()
			df['Adj Close'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[0])].squeeze()
			df['Volume'] = instancia.prices.loc[:, (ticker, instancia.tipo_precio[5])].squeeze()
			df.fillna(0, inplace=True)
			df[df < 0] = 0
			tickers_added += ticker + ', '
		except KeyError as e:
			print(f'Error al agregar precios para {ticker}: {e}')

	print(f'Se insertaron las columnas OHLCAV en los DF {tickers_added.rstrip(", ")}.')


def calc_prices_df(self, column_price):
	""" Crea un nuevo DF solo con un precio específico de todos los activos """

	prices_dict = {}
	tickers_added = []

	for ticker in self.tickers:
		# Trabajamos sobre una copia
		df = getattr(self, ticker).copy(deep=True)
		if column_price not in df.columns:
			raise KeyError(f'La columna {column_price} no existe en el DF {ticker}')
				
		price_values = df[column_price]
		
		prices_dict[ticker] = price_values
		tickers_added.append(ticker)
	
	prices_df = pd.DataFrame(prices_dict)
	print(f'El DF de {column_price}, fue creado con los activos {", ".join(tickers_added)}.')
	return prices_df


def calc_returns_df(self, method, column_price):
	""" Crea un nuevo DF con los returns de todos los activos """
	valid_methods = ['log', 'simple']
	if method not in valid_methods:
		raise ValueError(f'El método no es válido. Usar uno de: {", ".join(valid_methods)}')

	returns_dict = {}
	tickers_added = []

	for ticker in self.tickers:
		df = getattr(self, ticker)
		if column_price not in df.columns:
			raise KeyError(f'La columna {column_price} no existe en el DF {ticker}')
		
		if method == 'log':
			df['returns'] = np.log(df[column_price]).diff()
		else:
			df['returns'] = df[column_price].pct_change()
		
		df['returns'] = df['returns'].fillna(0)
		returns_dict[ticker] = df['returns']
		tickers_added.append(ticker)
	
	returns_df = pd.DataFrame(returns_dict)
	print(f'El DF de {method.capitalize()} Returns en función de {column_price}, fue creado con los activos {", ".join(tickers_added)}.')
	return returns_df


def calc_returns_volat_df(self, method, column_price, window=40, market_days_year=252):
	""" Creamos un nuevo DF con returns y volatilidad de todos los activos """
	valid_methods = ['log', 'simple']
	if method not in valid_methods:
		raise ValueError(f'El método no es válido. Usar uno de: {", ".join(valid_methods)}')
	
	returns_volat_dict = {}
	tickers_added = []

	for ticker in self.tickers:
		df = getattr(self, ticker)
		if column_price not in df.columns:
			raise KeyError(f'La columna {column_price} no existe en el DF {ticker}')

		if method == 'log':
			df['returns'] = np.log(df[column_price]).diff()
		else:
			df['returns'] = df[column_price].pct_change()
		
		df['returns'] = df['returns'].fillna(0)
		df['volat'] = (df['returns'].rolling(window=window).std().fillna(0)) * np.sqrt(market_days_year)

		returns_volat_dict[ticker + '_returns'] = df['returns']
		returns_volat_dict[ticker + '_volat_' + str(window)] = df['volat']
		tickers_added.append(ticker)

	returns_volat_df = pd.DataFrame(returns_volat_dict)
	print(f'Se creo el DF de {method.capitalize()} Returns en función de {column_price} y Volatilidad Anual con ventana de {window} ruedas.\nContiene los activos {", ".join(tickers_added)}.')
	return returns_volat_df


# def calculate_returns(df):
# 	"""	
# 	Parámetros:
# 	- df: DataFrame original.
# 	"""
# 	df[df < 0] = 0
# 	df['returns'] = np.log(df['Adj Close']).diff().fillna(0)
# 	msg = 'log returns sobre Adj Close en "returns"'

# 	# df['EMA1'] = df['Adj Close'].ewm(span=EMA1, adjust=False).mean()
# 	# df['EMA2'] = df['Adj Close'].ewm(span=EMA2, adjust=False).mean()
# 	return df, msg


def calculate_returns(df, method='log', column_price='Adj Close'):
	""" 
	Calcula los returns en funcion del metodo y precio. 
	Parámetros:
	- df: DataFrame original.
	"""
	valid_methods = ['log', 'simple']
	if method not in valid_methods:
		raise ValueError(f'El método no es válido. Usar uno de: {", ".join(valid_methods)}')

	if column_price not in df.columns:
		raise KeyError(f'La columna {column_price} no existe en el DF {ticker}')

	if method == 'log':
		df['log_returns'] = np.log(df[column_price]).diff().fillna(0)
	else:
		df['simple_returns'] = df[column_price].pct_change().fillna(0)

	msg = f'{method.capitalize()} Returns sobre {column_price} en "returns"'

	return df, msg


def calculate_volat(df, method='log', column_price='Adj Close', window=40, market_days_year=252):
	""" 
	Calcula la volatilidad en funcion del metodo y precio. 
	Parámetros:
	- df: DataFrame original.
	"""
	valid_methods = ['log', 'simple']
	if method not in valid_methods:
		raise ValueError(f'El método no es válido. Usar uno de: {", ".join(valid_methods)}')

	if column_price not in df.columns:
		raise KeyError(f'La columna {column_price} no existe en el DF {ticker}')
	
	if method == 'log':
		returns = np.log(df[column_price]).diff().fillna(0)
	else:
		returns = df[column_price].pct_change().fillna(0)
	
	df[f'volat_{window}'] = (returns.rolling(window=window).std().fillna(0)) * np.sqrt(market_days_year)

	msg = f'Volatilidad Anual con ventana de {window} ruedas en función de {method.capitalize()} Returns sobre {column_price} en "{"volat_" + str(window)}"'

	return df, msg



# La siguiente Function tiene como fin poder visualizar los DataFrames de Pandas con algunas ventajas.

# Saving the original Pandas method
_original_repr_html_ = pd.DataFrame._repr_html_


def show_df(content, width='99%', height='380px'):
	"""
	Displays a DataFrame or HTML in a scrollable container.
	"""
	num_rows, num_cols = content.shape if isinstance(content, pd.DataFrame) else (0, 0)
	content_html = content.to_html() if isinstance(content, pd.DataFrame) else str(content)
	
	styles = f"""
	<style>
		.scrollable-table-container {{ width: {width}; height: {height}; overflow-y: auto; border: 1px solid #ccc; padding: 8px; }} 
		table {{ width: 100%; border-collapse: collapse; text-align: left; }} 
		th, td {{ border: 1px solid #ddd; padding: 4.5px; height: 15px; vertical-align: middle; }} 
		th {{ position: sticky; top: 0; background-color: #8C8C8C; z-index: 2; }}
		th:first-child {{ position: sticky; left: 0; z-index: 1; }}
		.summary {{ margin-top: 7px; font-size: 13px; color: #D4D4D4; }}
	</style>
	"""
	
	html_content = f"""
	<div class="scrollable-table-container">{content_html}</div>
	<div class="summary">Totals = {num_rows} rows x {num_cols} columns</div>
	"""
	
	display(HTML(styles + html_content))


def auto_show_df(cls):
	"""
	Decorator overriding the _repr_html_ Pandas method to use the show_df function.
	"""
	def custom_repr(self):
		show_df(self)
		return ''
	
	cls._repr_html_ = custom_repr
	return cls


# pd.DataFrame = auto_show_df(pd.DataFrame)


# Function to revert to the original behavior
def undo_show_df():
	""" 
	The original pandas format is written again without restarting the kernel, only by calling the function.
	"""
	pd.DataFrame._repr_html_ = _original_repr_html_

	display(Javascript("""
		const styleElements = document.querySelectorAll('style');
		styleElements.forEach(el => {
			if (el.innerText.includes('.scrollable-table-container')) {
				el.remove();
			}
		});
	"""))
	


def mostrar_plotly_para_github(fig, ancho=800, alto=600):
	"""
	Muestra un gráfico de Plotly como imagen estática,
	ideal para que sea visible en GitHub.
	"""
	# # Exporta el gráfico como imagen PNG en memoria
	# img_bytes = fig.to_image(format="png", width=ancho, height=alto)
	
	# # Muestra la imagen en el notebook
	# # display(Image(img_bytes))
	# display(HTML(f'<img src="data:image/png;base64,{img_bytes.encode("base64").decode()}" />'))

	try:
		img_bytes = fig.to_image(format="png", engine="kaleido")
		display(Image(img_bytes))

		img_base64 = base64.b64encode(img_bytes).decode('utf-8')
		html = f'<img src="data:image/png;base64,{img_base64}"/>'
		display(HTML(html))
		
	except Exception as e:
		print("Error al intentar convertir la figura en imagen:")
		print(e)

