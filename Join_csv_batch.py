import pandas as pd
import geopandas as gpd
from qgis.core import QgsVectorLayer, QgsProject

# Caminhos para os arquivos
csv_path = 'C:/Users/Gustavo/Downloads/pib_mun_2020 (2).csv'
shp_path = 'C:/Users/Gustavo/Downloads/BR_Municipios_2022/BR_Municipios_2022.shp'
output_path = 'C:/Users/Gustavo/Downloads/BR_Municipios_PIB.shp'

## Carregar o shapefile como GeoDataFrame
gdf = gpd.read_file(shp_path)

# Carregar o CSV como DataFrame
df = pd.read_csv(csv_path)

# Verificar se as colunas-chave estão presentes
assert 'CD_MUN' in gdf.columns, "A coluna 'CD_MUN' não está presente no shapefile."
assert 'cd_mun' in df.columns, "A coluna 'cd_mun' não está presente no CSV."
assert 'ano' in df.columns, "A coluna 'ano' não está presente no CSV."
assert 'pib' in df.columns, "A coluna 'pib' não está presente no CSV."

# Converter a coluna 'pib' para o tipo decimal (float64)
df['pib'] = df['pib'].astype('float64')

# Converter as colunas 'CD_MUN' e 'cd_mun' para string
gdf['CD_MUN'] = gdf['CD_MUN'].astype(str)
df['cd_mun'] = df['cd_mun'].astype(str)

# Pivotar o DataFrame para que cada ano seja uma coluna
df_pivot = df.pivot(index='cd_mun', columns='ano', values='pib').reset_index()

# Renomear colunas pivotadas para 'PIB_Ano'
df_pivot.columns = ['cd_mun'] + [f'PIB_{int(col)}' for col in df_pivot.columns[1:]]

# Unir o GeoDataFrame com o DataFrame pivotado
gdf = gdf.merge(df_pivot, left_on='CD_MUN', right_on='cd_mun', how='left')

# Salvar o resultado como um novo shapefile
gdf.to_file(output_path, driver='ESRI Shapefile')

# Carregar o novo shapefile no QGIS
output_layer = QgsVectorLayer(output_path, "BR_Municipios_PIB", "ogr")
QgsProject.instance().addMapLayer(output_layer)

print("Junção concluída e shapefile salvo.")