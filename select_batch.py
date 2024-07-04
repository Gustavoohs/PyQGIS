import os
import glob
from qgis.core import QgsProject, QgsVectorLayer, QgsVectorFileWriter

# caminho dos arquivos shapefile
path = 'C:/Users/Gustavo/Downloads/DETER'

# nome do campo e possíveis valores do atributo que você deseja selecionar
attribute_field = 'SATELLITE'
attribute_values = ['AMAZONIA1', 'AMAZONIA-1']

# carregar os arquivos shapefile na lista de camadas do projeto
project = QgsProject.instance()
for file in glob.glob(os.path.join(path, '*.shp')):
    layer_name = os.path.splitext(os.path.basename(file))[0]
    layer = QgsVectorLayer(file, layer_name, 'ogr')
    
    if not layer.isValid():
        print(f"Erro ao carregar camada: {file}")
        continue
    
    project.addMapLayer(layer)

    # criar expressão para selecionar os recursos com base nos possíveis valores do atributo
    expression = f'("{attribute_field}" = \'{attribute_values[0]}\')'
    for value in attribute_values[1:]:
        expression += f' OR ("{attribute_field}" = \'{value}\')'
    
    # selecionar os recursos com base na expressão de consulta
    selection = layer.selectByExpression(expression)
    output_path = os.path.join(path, f'{layer_name}_selected.shp')
    QgsVectorFileWriter.writeAsVectorFormat(layer, output_path, 'utf-8', layer.crs(), 'ESRI Shapefile', onlySelected=True)
