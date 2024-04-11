# Importar os módulos necessários do PyQGIS
from qgis.core import QgsVectorLayer, QgsProject

# Carregar os arquivos vetoriais como camadas do QGIS
poligonos_path = 'C:/Users/Aluga.com/Downloads/poly.geojson'
feicoes_path = 'C:/Users/Aluga.com/Downloads/rings.geojson'

poligonos_layer = QgsVectorLayer(poligonos_path, 'Polígonos', 'ogr')
feicoes_layer = QgsVectorLayer(feicoes_path, 'Feições', 'ogr')

# Verificar se as camadas foram carregadas corretamente
if not poligonos_layer.isValid() or not feicoes_layer.isValid():
    print('Falha ao carregar camadas!')
    exit()

# Criar uma coluna para armazenar os atributos concatenados
poligonos_layer.dataProvider().addAttributes([QgsField('atributos_concatenados', QVariant.String)])
poligonos_layer.updateFields()

# Iterar sobre os polígonos
for poligono in poligonos_layer.getFeatures():

    # Filtrar as feições tocadas pelo polígono atual
    feicoes_tocadas = []
    for feicao in feicoes_layer.getFeatures():
        if poligono.geometry().intersects(feicao.geometry()):
            feicoes_tocadas.append(feicao['mrb_dist'])

    # Concatenar os atributos das feições tocadas
    atributos_concatenados = '; '.join(feicoes_tocadas)

    # Atualizar a coluna 'atributos_concatenados' do polígono
    poligonos_layer.startEditing()
    poligonos_layer.changeAttributeValue(poligono.id(), poligonos_layer.fields().indexFromName('atributos_concatenados'), atributos_concatenados)
    poligonos_layer.commitChanges()

# Adicionar a camada de polígonos ao projeto do QGIS
QgsProject.instance().addMapLayer(poligonos_layer)

# Visualizar o resultado no QGIS
iface.mapCanvas().refreshAllLayers()