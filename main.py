import geopandas as gpd
import numpy as np
import fiona
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from shapely import geos
from shapely.geometry import Point
from matplotlib.backends.backend_pdf import PdfPages


def point_to_geo(df, lon, lat):
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    df = df[df['lat'] > 0]
    df = df[df['lng'] > 0]
    datalist = list(zip(df[lon], df[lat]))
    plist = [Point(x[0], x[1]) for x in datalist]
    df['geometry'] = plist
    df = gpd.GeoDataFrame(df)  # 转换Geodataframe格式
    return df


with open("df_inst_rank.pickle", "rb") as fp:
    data = pickle.loads(fp.read())
nianlist = data["nian"]
nianlist = list(set(nianlist.values))
nianlist.sort()
# nianlist是数据集中的年列表
# data是要打点的数据
mapfile = "./gadm36_CHN_shp/gadm36_CHN_3.shp"
# datamap是地图数据
for nian in nianlist:
    with PdfPages(str(nian)+".pdf") as pdf:
        datamap = gpd.read_file(mapfile)
        f, ax = plt.subplots(1)
        niandata = data[data["nian"] == nian]
        niandata = point_to_geo(niandata, "lng", "lat")
        base = datamap.plot(ax=ax, color="white",
                            edgecolor="gray", figsize=(30, 30))
        niandata.plot(ax=base, marker="o", color="blue", markersize=3)
        pdf.savefig()
