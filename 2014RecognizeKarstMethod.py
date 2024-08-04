import geopandas as gpd
from shapely.geometry import Polygon
import pandas as pd
#--------------将等高线shp中闭合的线转为面---------------    
def Contour_To_Polygon(contour_lines_path,closed_contours_as_polygons_path):
    # 读取等高线数据
    contour_lines = gpd.read_file(contour_lines_path)

    # 创建一个空的GeoDataFrame来存储闭合的等高线面
    closed_contours_as_polygons = gpd.GeoDataFrame(columns=contour_lines.columns)

    # 遍历每一行等高线数据
    for index, row in contour_lines.iterrows():
        # 检查等高线是否闭合
        if row['geometry'].is_closed:
            # 将闭合的等高线转换为面
            polygon = Polygon(row['geometry'])
            # 创建一个临时的GeoDataFrame来存储这个面
            temp_gdf = gpd.GeoDataFrame([row], geometry=[polygon])
            # 将这个面添加到总的闭合等高线面的GeoDataFrame中
            closed_contours_as_polygons = pd.concat([closed_contours_as_polygons, temp_gdf])

    # 确保crs与原数据一致
    closed_contours_as_polygons.crs = contour_lines.crs

    # 保存闭合的等高线面为新的Shapefile文件
    closed_contours_as_polygons.to_file(closed_contours_as_polygons_path)
    print("闭合等高线转面成功")
    
# #--------------将等高线shp中闭合的线转为面---------------    
# contour_lines_path=    r"F:\VSCode\Terrain\data\0datasource\dem\广东\Contour_与polygonSupass30I清远JXK相交相交.shp"#Contour与Area10000相交2.shp"
# closed_contours_as_polygons_path=r"F:\VSCode\Terrain\data\0datasource\dem\广东\Contour_与polygonSupass30I清远JXK相交相交-转面.shp"#Contour与Area10000相交2-转面.shp"
# Contour_To_Polygon(contour_lines_path,closed_contours_as_polygons_path)


import geopandas as gpd
#---------------
def getCls_from_ContourPolygon(rectangles_path,polygons_path,feaName):
    # 读取两个图层
    rectangles = gpd.read_file(rectangles_path)
    polygons = gpd.read_file(polygons_path)

    # 检查矩形框图层中是否存在ClsNum1字段
    if feaName not in rectangles.columns:
        # 如果不存在，则添加一个名为ClsNum1的新字段，类型为字符串
        rectangles[feaName] = None  # 初始化为None，可以替换成其他默认值

        # 将新的字段写回到Shapefile中，确保字段类型为字符串
        rectangles.to_file(rectangles_path, driver='ESRI Shapefile')

        # 由于to_file操作可能改变字段类型，再次读取文件并确保字段类型为字符串
        rectangles = gpd.read_file(rectangles_path)

    # 遍历矩形框图层中的每一个要素
    for index, rectangle in rectangles.iterrows():
        # 选择与当前矩形框相交的多边形
        intersecting_polygons = polygons[polygons.intersects(rectangle['geometry'])]
        
        # 如果有相交的多边形
        if not intersecting_polygons.empty:
            # 找出面积最大的多边形
            max_area_polygon = intersecting_polygons.iloc[intersecting_polygons.area.argmax()]
            
            # 获取面积最大的多边形的feaName值
            cls_num1_value = max_area_polygon[feaName]
            
            # 将feaName值赋给矩形框图层的当前要素
            rectangles.at[index, feaName] = cls_num1_value

    # 保存更新后的矩形框图层
    rectangles.to_file(rectangles_path)
    print('完成getCls_from_ContourPolygon'+feaName)
    
feaName='ClsCenN12'
rectangles_path=r"F:\VSCode\Terrain\data\0datasource\dem\广东\juxingkuangTerrain论文中使用-基于规则20m等高距-清远112个.shp"
polygons_path=r"F:\VSCode\Terrain\data\0datasource\dem\广东\Contour_与polygonSupass30I清远JXK相交相交-转面-Join.shp"
getCls_from_ContourPolygon(rectangles_path,polygons_path,feaName)