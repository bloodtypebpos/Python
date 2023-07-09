import urllib.request
from bs4 import BeautifulSoup
#we import the data of both Italy, Covid and new_regions
import geopandas as gpd
import pandas as pd
import os
import matplotlib.pyplot as plt
from geopy import geocoders
from shapely.geometry import Point, Polygon
import openpyxl
import time

dbdir = r'C:\Users\Matt\Desktop\Italy'
os.chdir(dbdir)

fig, ax = plt.subplots(figsize=(10, 10))
crs = {'init': 'epsg:4326'}

color_array = ['#C62828', '#C62828', '#283593', '#FF9800', '#283593']
colors = []
for i in range(0, 20):
    colors.append(color_array[i%len(color_array)])


italy = gpd.read_file('italy.shp')
italy.crs = crs
italy['color'] = colors
italy.plot(ax=ax, color=italy['color'], aspect=1)


def getdata1():
    url = "https://www.atlasobscura.com/things-to-do/italy/places?page=2"
    url = "https://www.atlasobscura.com/things-to-do/italy/ruins?page=2"
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    bs_c1 = 'CardWrapper --PlaceWrapper js-CardWrapper '
    bs_c2 = 'Card --content-card-v2 --content-card-item Card--flat'
    bs_c3 = 'Card__img u-img-responsive --img-responsive --content-card-img lazyloaded'
    bs_c4 = 'Card__heading --content-card-v2-title js-title-content'

    attrs2 = ['data-city',
             'data-state',
             'data-lat',
             'data-lng',
             'href']

    attrs3 = ['src']
    attrs4 = ['span']

    divs = [bs_c2, bs_c3, bs_c4]
    attributes = [attrs2, attrs3, attrs4]

    titles = []
    infos = []
    imgs = []
    # get text
    text = soup.get_text()
    mydivs = soup.find_all("h3", {"class": f'{bs_c4}'})
    for div in mydivs:
        titles.append(div.text)
    mydivs = soup.find_all("a", {"class": f'{bs_c2}'})
    for div in mydivs:
        info = []
        for attr in attrs2:
            info.append(div.get(attr))
        infos.append(info)
        stuff = getattr(div, 'contents')
        for s in stuff:
            if 'img alt' in str(s):
                img = str(s).split('data-src="')[1]
                img = img.split('"')[0]
                imgs.append(img)
    for i in range(0, len(titles)):
        print(titles[i])
        for j in range(0, len(attrs2)):
            print(f'{attrs2[j]}: {infos[i][j]}')
        print(imgs[i])
        print("=====================================================================")



italy['NOME_REG'][0] = "PIEDMONTE"
italy['NOME_REG'][1] = "AOSTA"
italy['NOME_REG'][3] = "TRENTINO"
print(italy.head())
print(len(italy))
headers = italy.columns.tolist()
states = []
for header in headers:
    print(header)
print("==============================================================")
for i in range(len(italy)):
    states.append(italy['NOME_REG'][i])
for state in states:
    print(state)
print("-------------------------")

def sad_excursion():
    gn = geocoders.GeoNames(username='bloodtypebpos')
    italy_lats = []
    italy_lngs = []
    for i in range(len(states)):
        try:
            loc = gn.geocode(f'{states[i]}, Italy')
            italy_lats.append(loc.raw['lat'])
            italy_lngs.append(loc.raw['lng'])
        except:
            print(states[i])
            italy_lats.append(45.0522)
            italy_lngs.append(7.5154)

    for i in range(len(states)):
        plt.text(italy_lats[i], italy_lngs[i], states[i])


italy['coords'] = italy['geometry'].apply(lambda x: x.representative_point().coords[:])
italy['coords'] = [coords[0] for coords in italy['coords']]
for idx, row in italy.iterrows():
    plt.text(row['coords'][0], row['coords'][1], row['NOME_REG'],
             # bbox={'facecolor': 'white', 'alpha': 0.2, 'pad': 1, 'edgecolor': 'none'},
             horizontalalignment='center')

wb = openpyxl.load_workbook('template.xlsx')
sht = wb['Sheet1']

group_val = 'I' # g, h, i... T is end
groups = [sht[f'{group_val}1'].value]

url_begin = "https://www.atlasobscura.com/things-to-do/italy/"
url_end = "?page="
url = "https://www.atlasobscura.com/things-to-do/italy/places?page=2"
url = "https://www.atlasobscura.com/things-to-do/italy/ruins?page=2"

rownum = 2
for group in groups:
    print(group)
    page_num = 1
    page_bool = True
    while(page_bool):
        try:
            time.sleep(3)
            url = f'{url_begin}{group}{url_end}{page_num}'
            print(url)
            page_num = page_num + 1
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            bs_c2 = 'Card --content-card-v2 --content-card-item Card--flat'
            bs_c3 = 'Card__img u-img-responsive --img-responsive --content-card-img lazyloaded'
            bs_c4 = 'Card__heading --content-card-v2-title js-title-content'
            attrs = ['data-city',
                     'data-state',
                     'data-lat',
                     'data-lng',
                     'href']
            titles = []
            infos = []
            imgs = []
            links = []
            # get text
            text = soup.get_text()
            mydivs = soup.find_all("h3", {"class": f'{bs_c4}'})
            for div in mydivs:
                titles.append(div.text)
            mydivs = soup.find_all("a", {"class": f'{bs_c2}'})
            for div in mydivs:
                info = []
                for attr in attrs:
                    info.append(div.get(attr))
                infos.append(info)
                stuff = getattr(div, 'contents')
                for s in stuff:
                    if 'img alt' in str(s):
                        img = str(s).split('data-src="')[1]
                        img = img.split('"')[0]
                        imgs.append(img)

            scalerx = 87000   # 80000
            scalery = 110000  # 100000
            xx = 289442    # xx = 200000
            yy = 42500    # yy = 454081
            lats = [41.9040, 43.7237, 40.8499, 41.1173, 42.4625, 38.1142, 37.0756, 43.8163, 45.4420, 36.6470]
            lngs = [12.4823, 10.4006, 14.2613, 16.8728, 14.2149, 13.3607, 15.2856,  7.7752, 12.3152, 15.0797]

            lats = [lat*scalery + yy for lat in lats]
            lngs = [lng*scalerx - xx for lng in lngs]
            #print(min(lats))
            #print(max(lats))
            # rome, pisa, naples, bari, pescara, palermo, syracuse, sanremo, venice, bottom!

            for i in range(0, len(titles)):
                #print(titles[i])
                sht[f'A{i+rownum}'].value = titles[i]
                sht[f'B{i+rownum}'].value = infos[i][0]
                sht[f'C{i+rownum}'].value = infos[i][1]
                #sht[f'D{i+2}'].value = lats[i % len(lats)]
                #sht[f'E{i+2}'].value = lngs[i % len(lngs)]
                #sht[f'D{i+2}'].value = float(infos[i][2])*scalery + yy
                #sht[f'E{i+2}'].value = float(infos[i][3])*scalerx - xx
                sht[f'D{i+rownum}'].value = infos[i][2]
                sht[f'E{i+rownum}'].value = infos[i][3]
                sht[f'F{i+rownum}'].value = imgs[i]
                sht[f'{group_val}{i+rownum}'].value = "1"
                sht[f'V{i+rownum}'].value = f'https://www.atlasobscura.com{infos[i][4]}'
                #for j in range(0, len(attrs)):
                #    print(f'{attrs[j]}: {infos[i][j]}')
                #lats.append(infos[i][2])
                #lngs.append(infos[i][3])
                #print(imgs[i])
                #print("=====================================================================")
            rownum = rownum + len(titles)
            print('end')
        except:
            page_bool = False
        print("==========================================================")


wb.save(f'{groups[0]}.xlsx')
# geometry = [Point(xy) for xy in zip(lats, lngs)]

def nottoday():
    data = pd.read_excel(r'output.xlsx', 'Sheet1')

    #geometry = [Point(xy) for xy in zip((data["data-lat"]*scaler-xx), (data["data-lng"]*scaler + yy))]
    #geometry = [Point(xy) for xy in zip((data["data-lng"]*scalerx-xx), (data["data-lat"]*scalery + yy))]
    geometry = [Point(xy) for xy in zip((data["data-lng"]), (data["data-lat"]))]
    #print(geometry)

    geodata = gpd.GeoDataFrame(data, crs=crs, geometry=geometry)
    #geodata.crs = crs
    geodata.plot(ax=ax, color='black', markersize=50, aspect=1)
    geodata.plot(ax=ax, color='white', markersize=25, aspect=1)

    plt.show()

