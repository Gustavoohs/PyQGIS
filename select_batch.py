import os
import glob
from qgis.core import QgsProject, QgsExpression, QgsFeatureRequest, QgsVectorLayer, QgsVectorFileWriter,QgsExpressionContextScope

# caminho dos arquivos shapefile
path = 'C:/Users/Gustavo/Downloads/DETER'

# nome do campo e valor do atributo que você deseja selecionar
attribute_field = 'SATELLITE'
attribute_value = 'AMAZONIA1'

# carregar os arquivos shapefile na lista de camadas do projeto
project = QgsProject.instance()
for file in glob.glob(os.path.join(path, '*.shp')):
    layer_name = os.path.splitext(os.path.basename(file))[0]
    layer = QgsVectorLayer(file, layer_name, 'ogr')
    project.addMapLayer(layer)

    # selecionar os recursos com base na expressão de consulta
    selection = layer.selectByExpression(f'"{attribute_field}" = \'{attribute_value}\'')
    output_path = os.path.join(path, f'{layer_name}_selected.shp')
    QgsVectorFileWriter.writeAsVectorFormat(layer, output_path, 'utf-8', layer.crs(), 'ESRI Shapefile', onlySelected=True)
    
    
    