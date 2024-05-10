import os
import geopandas as gpd
from shapely.geometry import Polygon
import fiona

def create_grid_shapefile(folder_path, output_shapefile):
    # 获取文件夹下所有的 HDF 文件路径
    # hdf_files = [f for f in os.listdir(folder_path) if f.endswith('.hdf')]
    hdf_files = pd.read_csv(folder_path)
    hdf_files.sort_values(by='filename', inplace=True)
    # 定义一个空的 GeoDataFrame 用于存储格网范围数据
    gdf = gpd.GeoDataFrame(columns=['filename', 'geometry'])
    
    for filename in hdf_files['filename']:
        # 提取经纬度范围信息
        print(filename)
        if 'default' in filename:
            continue
        h_index = int(filename[16:18])
        v_index = int(filename[19:21])
        
        # 计算经纬度范围
        lon_max = h_index * 5 - 180
        lon_min = lon_max - 5
        lat_max = v_index * 5 - 90
        lat_min = lat_max - 5
        
        # 创建格网范围的多边形
        polygon = Polygon([(lon_min, lat_min), (lon_min, lat_max), 
                           (lon_max, lat_max), (lon_max, lat_min)])
        
        # 将格网范围添加到 GeoDataFrame 中
        gdf = gdf.append({'filename': filename, 'geometry': polygon}, ignore_index=True)
    
    # 将结果保存为 Shapefile 文件
    gdf.crs = "EPSG:4326"  # 设置坐标系为 WGS84
    gdf.to_file(output_shapefile, driver="ESRI Shapefile")

# 调用函数创建格网范围的 Shapefile 文件
create_grid_shapefile(input_folder, output_shapefile)
