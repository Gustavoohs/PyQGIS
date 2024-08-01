import pandas as pd
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsWkbTypes, edit
from PyQt5.QtCore import QVariant

# Caminho para o arquivo .gpkg e .xlsx
caminho_arquivo = 'C:/Users/Gustavo/Downloads/BR.gpkg'
caminho_excel = 'C:/Users/Gustavo/Downloads/pib_real_br (1) (1).xlsx'

# Ler o arquivo Excel usando pandas
df = pd.read_excel(caminho_excel)

# Criação de dicionário com os valores do PIB por ano
pib_data = df.set_index('ano')['pib_br_milhoes2020'].to_dict()

# Lista de campos a serem criados
fields = [
    QgsField('PIB_2002', QVariant.Double),
    QgsField('PIB_2003', QVariant.Double),
    QgsField('PIB_2004', QVariant.Double),
    QgsField('PIB_2005', QVariant.Double),
    QgsField('PIB_2006', QVariant.Double),
    QgsField('PIB_2007', QVariant.Double),
    QgsField('PIB_2008', QVariant.Double),
    QgsField('PIB_2009', QVariant.Double),
    QgsField('PIB_2010', QVariant.Double),
    QgsField('PIB_2011', QVariant.Double),
    QgsField('PIB_2012', QVariant.Double),
    QgsField('PIB_2013', QVariant.Double),
    QgsField('PIB_2014', QVariant.Double),
    QgsField('PIB_2015', QVariant.Double),
    QgsField('PIB_2016', QVariant.Double),
    QgsField('PIB_2017', QVariant.Double),
    QgsField('PIB_2018', QVariant.Double),
    QgsField('PIB_2019', QVariant.Double),
    QgsField('PIB_2020', QVariant.Double)
]

# Abre o GeoPackage
gpkg_layer = QgsVectorLayer(caminho_arquivo, 'BR', 'ogr')

if not gpkg_layer.isValid():
    print("Erro ao carregar a camada.")
else:
    # Adicionar os campos à camada
    with edit(gpkg_layer):
        for field in fields:
            gpkg_layer.addAttribute(field)
        gpkg_layer.updateFields()
    
    # Itera sobre todas as feições e atualiza os valores
    features = gpkg_layer.getFeatures()
    with edit(gpkg_layer):
        for feature in features:
            for field in fields:
                # Extrai o ano do nome do campo, por exemplo, 'PIB_2002' -> 2002
                ano = int(field.name().split('_')[1])
                # Atribui o valor correspondente do dicionário, se existir, senão 0.0
                pib_value = pib_data.get(ano, 0.0)
                feature.setAttribute(field.name(), pib_value)
            gpkg_layer.updateFeature(feature)
    
    # Salva as mudanças no arquivo
    gpkg_layer.commitChanges()

# Imprime os nomes dos campos para verificar se foram adicionados corretamente
print([novos_campos.name() for novos_campos in gpkg_layer.fields()])
