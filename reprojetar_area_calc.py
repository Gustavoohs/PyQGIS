# Bibliotecas
from qgis.core import QgsProject, QgsVectorLayer, QgsField
from PyQt5.QtCore import QVariant
import os
import processing

# Caminho onde os arquivos GPKG reprojetados serão salvos
output_directory = "C:/seu/caminho/destino"  # Altere para o seu caminho de destino

# EPSG para o qual você deseja reprojetar
crs_target = QgsCoordinateReferenceSystem(102033)  # ESRI:102033

# Itera sobre todas as camadas vetoriais carregadas no projeto
for layer in QgsProject.instance().mapLayers().values():
    if isinstance(layer, QgsVectorLayer) and layer.geometryType() == QgsWkbTypes.PolygonGeometry:
        # Reprojetar camada
        params = {
            'INPUT': layer,
            'TARGET_CRS': crs_target,
            'OUTPUT': 'memory:'  # Salva na memória
        }
        result = processing.run("native:reprojectlayer", params)
        reprojected_layer = result['OUTPUT']
        
        # Adiciona campo 'area_ha'
        reprojected_layer.startEditing()
        if 'area_ha' not in [field.name() for field in reprojected_layer.fields()]:
            reprojected_layer.addAttribute(QgsField('area_ha', QVariant.Double))
        reprojected_layer.updateFields()
        
        # Calcula área em hectares e preenche o campo
        for feature in reprojected_layer.getFeatures():
            area_m2 = feature.geometry().area()
            area_ha = area_m2 / 10000  # Converte m² para hectares
            reprojected_layer.changeAttributeValue(feature.id(), reprojected_layer.fields().indexFromName('area_ha'), area_ha)
        
        reprojected_layer.commitChanges()
        
        # Definir o nome do arquivo com o sufixo "_reprojetado"
        layer_name = layer.name()  # Pega o nome original da camada
        output_path = os.path.join(output_directory, f"{layer_name}_reprojetado.gpkg")
        
        # Exportar a camada reprojetada para GeoPackage
        QgsVectorFileWriter.writeAsVectorFormatV2(
            reprojected_layer,
            output_path,
            QgsCoordinateTransformContext(),
            QgsVectorFileWriter.SaveVectorOptions()
        )
        
        print(f"Camada {layer_name} salva como {output_path}")