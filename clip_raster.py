import os
from osgeo import gdal, ogr
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject
import processing

# Caminho para o shapefile de recorte
shapefile_path = "C:/Users/Gustavo/Downloads/teste.shp"

# Caminho para a pasta com as imagens .tif
imagem_folder = "C:/Users/Gustavo/Documents/Imagens"

# Carregar o shapefile
shapefile_layer = QgsVectorLayer(shapefile_path, 'shapefile', 'ogr')

# Verificar se o shapefile foi carregado corretamente
if not shapefile_layer.isValid():
    print('Erro ao carregar o shapefile')
else:
    # Listar os arquivos .tif na pasta
    tif_files = [f for f in os.listdir(imagem_folder) if f.endswith('.tif')]
    
    # Iterar sobre os arquivos .tif
    for tif_file in tif_files:
        # Caminho completo para o arquivo .tif
        tif_path = os.path.join(imagem_folder, tif_file)
        
        # Carregar a imagem raster
        raster_layer = QgsRasterLayer(tif_path, tif_file)
        
        # Verificar se a imagem raster foi carregada corretamente
        if not raster_layer.isValid():
            print(f'Erro ao carregar a imagem raster {tif_file}')
        else:
            # Nome para a nova imagem recortada
            output_path = os.path.join(imagem_folder, f'recortada_{tif_file}')
            
            # Recortar a imagem raster com base no shapefile
            result = processing.run("gdal:cliprasterbymasklayer", 
                           {'INPUT': raster_layer, 
                            'MASK': shapefile_layer, 
                            'OUTPUT': output_path})
            
            if result['OUTPUT']:
                print(f'Imagem {tif_file} recortada com sucesso')
            else:
                print(f'Erro ao recortar a imagem {tif_file}')
        # Limpar o cache do QGIS
        QgsProject.instance().clear()