import json
import requests
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
from math import cos, asin, sqrt, pi
import streamlit as st
from copy import deepcopy

gmaps_key = st.secrets["gmaps_key"]

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# actual api key and other parameters to pass in the search request such as the center location and radius of our search area
# center point for Munich is given in the lat/long below along with the search radius we are using
api_key = gmaps_key
center_lat = 48.137154
center_lng = 11.576124
radius = 15000

# Function to calculate distance in Km between two latitude/longitude points 
def lat_lon_distance(lat1, lon1, lat2, lon2):
    r = 6371 # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))

# function to convert a zip code returned from Google maps to a District so we can join with other data based on the distrtict if needed

def map_zip_dist(zip):
    zip_dist_dict = {
        80995 : 'Allach-Untermenzing',
        80997 : 'Allach-Untermenzing',
        80999 : 'Allach-Untermenzing',
        81247 : 'Allach-Untermenzing',
        81249 : 'Allach-Untermenzing',
        80331 : 'Altstadt-Lehel',
        80333 : 'Altstadt-Lehel',
        80335 : 'Altstadt-Lehel',
        80336 : 'Altstadt-Lehel',
        80469 : 'Altstadt-Lehel',
        80538 : 'Altstadt-Lehel',
        80539 : 'Altstadt-Lehel',
        81541 : 'Au-Haidhausen',
        81543 : 'Au-Haidhausen',
        81667 : 'Au-Haidhausen',
        81669 : 'Au-Haidhausen',
        81671 : 'Au-Haidhausen',
        81675 : 'Au-Haidhausen',
        81677 : 'Au-Haidhausen',
        81243 : 'Aubing-Lochhausen-Langwied',
        81245 : 'Aubing-Lochhausen-Langwied',
        81248 : 'Aubing-Lochhausen-Langwied',
        81249 : 'Aubing-Lochhausen-Langwied',
        81671 : 'Berg am Laim',
        81673 : 'Berg am Laim',
        81735 : 'Berg am Laim',
        81825 : 'Berg am Laim',
        81675 : 'Bogenhausen',
        81677 : 'Bogenhausen',
        81679 : 'Bogenhausen',
        81925 : 'Bogenhausen',
        81927 : 'Bogenhausen',
        81929 : 'Bogenhausen',
        80933 : 'Feldmoching-Hasenbergl',
        80935 : 'Feldmoching-Hasenbergl',
        80995 : 'Feldmoching-Hasenbergl',
        80689 : 'Hadern',
        81375 : 'Hadern',
        81377 : 'Hadern',
        80686 : 'Laim',
        80687 : 'Laim',
        80689 : 'Laim',
        80335 : 'Ludwigsvorstadt-Isarvorstadt',
        80336 : 'Ludwigsvorstadt-Isarvorstadt',
        80337 : 'Ludwigsvorstadt-Isarvorstadt',
        80469 : 'Ludwigsvorstadt-Isarvorstadt',
        80333 : 'Maxvorstadt',
        80335 : 'Maxvorstadt',
        80539 : 'Maxvorstadt',
        80636 : 'Maxvorstadt',
        80797 : 'Maxvorstadt',
        80798 : 'Maxvorstadt',
        80799 : 'Maxvorstadt',
        80801 : 'Maxvorstadt',
        80802 : 'Maxvorstadt',
        80807 : 'Milbertshofen-Am Hart',
        80809 : 'Milbertshofen-Am Hart',
        80937 : 'Milbertshofen-Am Hart',
        80939 : 'Milbertshofen-Am Hart',
        80637 : 'Moosach',
        80638 : 'Moosach',
        80992 : 'Moosach',
        80993 : 'Moosach',
        80997 : 'Moosach',
        80634 : 'Neuhausen-Nymphenburg',
        80636 : 'Neuhausen-Nymphenburg',
        80637 : 'Neuhausen-Nymphenburg',
        80638 : 'Neuhausen-Nymphenburg',
        80639 : 'Neuhausen-Nymphenburg',
        81539 : 'Obergiesing',
        81541 : 'Obergiesing',
        81547 : 'Obergiesing',
        81549 : 'Obergiesing',
        80687 : 'Pasing-Obermenzing',
        80689 : 'Pasing-Obermenzing',
        81241 : 'Pasing-Obermenzing',
        81243 : 'Pasing-Obermenzing',
        81245 : 'Pasing-Obermenzing',
        81247 : 'Pasing-Obermenzing',
        81539 : 'Ramersdorf-Perlach',
        81549 : 'Ramersdorf-Perlach',
        81669 : 'Ramersdorf-Perlach',
        81671 : 'Ramersdorf-Perlach',
        81735 : 'Ramersdorf-Perlach',
        81737 : 'Ramersdorf-Perlach',
        81739 : 'Ramersdorf-Perlach',
        80538 : 'Schwabing-Freimann',
        80801 : 'Schwabing-Freimann',
        80802 : 'Schwabing-Freimann',
        80803 : 'Schwabing-Freimann',
        80804 : 'Schwabing-Freimann',
        80805 : 'Schwabing-Freimann',
        80807 : 'Schwabing-Freimann',
        80939 : 'Schwabing-Freimann',
        80796 : 'Schwabing-West',
        80797 : 'Schwabing-West',
        80798 : 'Schwabing-West',
        80799 : 'Schwabing-West',
        80801 : 'Schwabing-West',
        80803 : 'Schwabing-West',
        80804 : 'Schwabing-West',
        80809 : 'Schwabing-West',
        80335 : 'Schwanthalerhöhe',
        80339 : 'Schwanthalerhöhe',
        80336 : 'Sendling',
        80337 : 'Sendling',
        80469 : 'Sendling',
        81369 : 'Sendling',
        81371 : 'Sendling',
        81373 : 'Sendling',
        81379 : 'Sendling',
        80686 : 'Sendling-Westpark',
        81369 : 'Sendling-Westpark',
        81373 : 'Sendling-Westpark',
        81377 : 'Sendling-Westpark',
        81379 : 'Sendling-Westpark',
        81379 : 'Thalkirchen-Obersendling-Fürstenried-Forstenried-Solln',
        81475 : 'Thalkirchen-Obersendling-Fürstenried-Forstenried-Solln',
        81476 : 'Thalkirchen-Obersendling-Fürstenried-Forstenried-Solln',
        81477 : 'Thalkirchen-Obersendling-Fürstenried-Forstenried-Solln',
        81479 : 'Thalkirchen-Obersendling-Fürstenried-Forstenried-Solln',
        81735 : 'Trudering-Riem',
        81825 : 'Trudering-Riem',
        81827 : 'Trudering-Riem',
        81829 : 'Trudering-Riem',
        81543 : 'Untergiesing-Harlaching',
        81545 : 'Untergiesing-Harlaching',
        81547 : 'Untergiesing-Harlaching'
    }
    return zip_dist_dict.get(zip)

def map_geo_dist(row): 
    dist_dict = {
        "23 Allach - Untermenzing" : "Allach-Untermenzing",
        "01 Altstadt - Lehel" : "Altstadt-Lehel",
        "05 Au - Haidhausen" : "Au-Haidhausen",
        "22 Aubing - Lochhausen - Langwied" : "Aubing-Lochhausen-Langwied",
        "14 Berg am Laim" : "Berg am Laim",
        "13 Bogenhausen" : "Bogenhausen",
        "24 Feldmoching - Hasenbergl" : "Feldmoching-Hasenbergl",
        "20 Hadern" : "Hadern",
        "25 Laim" : "Laim",
        "02 Ludwigsvorstadt - Isarvorstadt" : "Ludwigsvorstadt-Isarvorstadt",
        "03 Maxvorstadt" : "Maxvorstadt",
        "11 Milbertshofen - Am Hart" : "Milbertshofen-Am Hart",
        "10 Moosach" : "Moosach",
        "09 Neuhausen - Nymphenburg" : "Neuhausen-Nymphenburg",
        "17 Obergiesing - Fasangarten" : "Obergiesing-Fasangarten",
        "21 Pasing - Obermenzing" : "Pasing-Obermenzing",
        "16 Ramersdorf - Perlach" : "Ramersdorf-Perlach",
        "12 Schwabing - Freimann" : "Schwabing-Freimann",
        "04 Schwabing - West" : "Schwabing-West",
        "08 Schwanthalerhöhe" : "Schwanthalerhöhe",
        "06 Sendling" : "Sendling",
        "07 Sendling - Westpark" : "Sendling-Westpark",
        "19 Thalkirchen - Obersendling - Forstenried - Fürstenried - Solln" : "Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln",
        "15 Trudering - Riem" : "Trudering-Riem",
        "18 Untergiesing - Harlaching" : "Untergiesing-Harlaching"
    }
    return dist_dict.get(row['Raumbezug'])

def district_center_point(dist): 
    center_point = {
        "Allach-Untermenzing" : [48.19416, 11.46449],
        "Altstadt-Lehel" : [48.133249, 11.583058],
        "Au-Haidhausen" : [48.1286, 11.60457],
        "Aubing-Lochhausen-Langwied" : [48.140922, 11.424744],
        "Berg am Laim" : [48.13154, 11.624445],
        "Bogenhausen" : [48.16512, 11.6449],
        "Feldmoching-Hasenbergl" : [48.2098, 11.55305],
        "Hadern" : [48.120347, 11.482445],
        "Laim" : [48.138375, 11.504377],
        "Ludwigsvorstadt-Isarvorstadt" : [48.131951, 11.558724],
        "Maxvorstadt" : [48.14987, 11.56625],
        "Milbertshofen-Am Hart" : [48.197578, 11.577708],
        "Moosach" : [48.18207, 11.53426],
        "Neuhausen-Nymphenburg" : [48.15018, 11.54455],
        "Obergiesing-Fasangarten" : [48.103428, 11.589998],
        "Pasing-Obermenzing" : [48.15257, 11.47626],
        "Ramersdorf-Perlach" : [48.09892, 11.64604],
        "Schwabing-Freimann" : [48.157565, 11.58379],
        "Schwabing-West" : [48.15799, 11.5624],
        "Schwanthalerhöhe" : [48.14086, 11.56182],
        "Sendling" : [48.137262, 11.56004],
        "Sendling-Westpark" : [48.11674, 11.53231],
        "Thalkirchen-Obersendling-Forstenried-Fürstenried-Solln" : [48.09458, 11.5126],
        "Trudering-Riem" : [48.11264, 11.64991],
        "Untergiesing-Harlaching" : [48.116673, 11.572642]
    }
    return center_point.get(dist)

def convert_str_float(str_series):
    float_vals = []
    for s in str_series:
        if isinstance(s, str):
            float_vals.append(float(s.replace(",",".")))
        else:
            float_vals.append(s)
    return float_vals

@st.cache_data
def search_google_places(search_str):
    next_page_token = ""
    search_data = []
    while next_page_token is not None:
        # get method of requests module, return response object
        req = requests.get(url + "location=" + str(center_lat) + "%2C" + str(center_lng) + "&query=" + search_str + "&radius=" + str(radius) + "&key=" + gmaps_key+ "&pagetoken=" + next_page_token)
        
        # json method of response object: json format data -> python format data
        places_json = req.json()
        
        # Json results with our search results from Google maps
        my_result = places_json.get("results")
        next_page_token = places_json.get("next_page_token")
        for result in my_result:
            name = result.get('name')
            address = result.get('formatted_address')
            zip = result.get('formatted_address').split(', ')[1].split()[0]
            district = map_zip_dist(int(zip))
            lat = result.get('geometry').get('location').get('lat')
            lng = result.get('geometry').get('location').get('lng')
            dist_from_center = lat_lon_distance(center_lat, center_lng, result.get('geometry').get('location').get('lat'), result.get('geometry').get('location').get('lng'))
            rating = result.get('rating')
            num_ratings = result.get('user_ratings_total')
            search_data.append([name, address, zip, district, lat, lng, dist_from_center, rating, num_ratings])

        # Introducing 5 sec delay so the next page token is available on the server side
        time.sleep(5)

    return pd.DataFrame(search_data, columns=['name', 'address', 'zip', 'district', 'lat', 'lng', 'dist_from_center', 'rating', 'num_ratings']).dropna().reset_index(drop=True)

# Get Lidl and Aldi locations data from Google Places API
lidl_df = search_google_places(search_str="lidl")
aldi_df = search_google_places(search_str="aldi")


# Import the GeoJson data for Munich
with open("./data/neighbourhoods_munich.geojson") as response:
    munich = json.load(response)

# Import data we collected from https://www.muenchen.de/
# Import Unemployment Data and filter for unemployment rate and male and female records only
df1 = pd.read_csv("./data/export_ar.csv")
df_labour = df1[
                (df1['Indikator'] == "Arbeitslose - Anteil") & 
                ((df1['Name Basiswert 1'] == "Arbeitslose (männlich)") | (df1['Name Basiswert 1'] == "Arbeitslose (weiblich)"))
                ]
df_labour['unemp_rate'] = convert_str_float(df_labour['Indikatorwert'])
df_labour['Name'] = df_labour.apply(map_geo_dist, axis=1)
df_sum_labour = df_labour.dropna().groupby(['Name', 'Jahr']).agg({'unemp_rate': 'mean'}).reset_index()

# Import Population Data
df2 = pd.read_csv("./data/export_be.csv")
df_population = df2[df2['Indikator'] == "Bevölkerungsdichte"]

df_population['population'] = convert_str_float(df_population['Indikatorwert'])
df_population['Name'] = df_population.apply(map_geo_dist, axis=1)
#df_sum_pop = df_population.dropna().groupby(['Name', 'Jahr']).agg({'pop_density': 'sum'}).reset_index()
df_population.dropna().reset_index()

df_data = df_population.merge(df_sum_labour)

df_growth = pd.read_csv("./data/pop_unemp_growth.csv")

st.header("Supermarket stores in Munich")
st.subheader("Lidl stores shown in :red[Red] and Aldi stores in :orange[Orange]", )
tab1, tab2 = st.tabs(["Demographics Change Animation", "Demographics by District"])

with tab1:
    show_data1 = st.checkbox(label="Include data table with visual")
    left_column1, right_column1 = st.columns([1,1])
    metric1 = left_column1.radio(label='Metric:', options=['Population','Unemployment Rate'])
    #metric_year = right_column.selectbox(label="As of Year", options=sorted(pd.unique(df_data["Jahr"]), reverse=True))
    zoom_dist1 = right_column1.selectbox(label="Zoom to District", options=["None"]+sorted(pd.unique(df_data["Name"])))

    if metric1 == "Population":
        color_df_field1 = "population"
        color_scale1 = "Blues"
    else:
        color_df_field1 = "unemp_rate"
        color_scale1 = "Mint"

    if zoom_dist1 == "None":
        center_lat1 = 48.137154
        center_lng1 = 11.576124
        zoom_index1 = 10
    else:
        center_lat1 = district_center_point(zoom_dist1)[0]
        center_lng1 = district_center_point(zoom_dist1)[1]
        zoom_index1 = 11

    #df_filtered = df_data[df_data['Jahr'] == metric_year][["Indikator","Jahr","Name","population","unemp_rate"]]
    df_filtered1 = df_data[["Indikator","Jahr","Name","population","unemp_rate"]].sort_values(by=["Jahr","Name"], ascending=True)
    fig1 = px.choropleth_mapbox(df_filtered1, geojson=munich,
                            color = color_df_field1,
                            color_continuous_scale = color_scale1,
                            locations="Name", featureidkey="properties.Name",
                            center={"lat": center_lat1, "lon": center_lng1},
                            animation_frame="Jahr", animation_group="Name"
                            )

    #Adding the Lidl points  
    fig1.add_trace(go.Scattermapbox(
        lat=lidl_df['lat'],
        lon=lidl_df['lng'],
        mode='markers',
        marker=dict(size=11, color='rgb(166, 10, 61)'),
        text=lidl_df[['name', 'address', 'zip', 'district']].apply(lambda row: '<br>'.join(row), axis=1),
        name='Lidl', 
        line=dict(color='black', width=2)
    ))

    #Adding the Aldi points
    fig1.add_trace(go.Scattermapbox(
        lat=aldi_df['lat'],
        lon=aldi_df['lng'],
        mode='markers',
        marker=dict(size=12, color='rgb(224, 152, 33)'),
        text=aldi_df[['name', 'address', 'zip', 'district']].apply(lambda row: '<br>'.join(row), axis=1),
        name='Aldi',
        line=dict(color='black', width=2)
    ))

    #Updating Layout
    fig1.update_layout(
        margin={"r": 0.2, "t": 0.2, "l": 0.2, "b": 0.2},
        title="Store Locations in Munich",
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lng,),
            zoom=zoom_index1,
        ),
        height=600,
        width=970,
        legend=dict(
            x=0.9,  
            y=0.95,
            font=dict(
                family='sans-serif',
                size=14,
                color='black'
            ),
            bgcolor='rgba(230, 230, 230, 0.8)', 
            bordercolor='black',
            borderwidth=2
        )
    )

    st.plotly_chart(fig1)

    if show_data1:
        #st.subheader(f"{metric} data by district for year {metric_year}:")
        st.subheader("Data Table:")
        st.dataframe(data=df_filtered1)

with tab2:
    show_data2 = st.checkbox(label="Include data table")
    left_column2, right_column2 = st.columns([1,1])

    metric2 = left_column2.radio(label='Metric: ', options=['Population','Unemployment Rate'])
    metric_year2 = right_column2.selectbox(label="Growth Timeframe", options=sorted(pd.unique(df_growth["Growth_timeframe"]), reverse=False))

    if metric2 == "Population":
        color_df_field2 = "pop_dif"
        color_scale2 = "Blues"
    else:
        color_df_field2 = "unemp_dif"
        color_scale2 = "Mint"

    df_filtered2 = df_growth[df_growth['Growth_timeframe'] == metric_year2]
    fig2 = px.choropleth_mapbox(df_filtered2, geojson=munich,
                            color = color_df_field2,
                            color_continuous_scale = color_scale2,
                            locations="Name", featureidkey="properties.Name",
                            center={"lat": center_lat, "lon": center_lng}
                            )

    #Adding the Lidl points  
    fig2.add_trace(go.Scattermapbox(
        lat=lidl_df['lat'],
        lon=lidl_df['lng'],
        mode='markers',
        marker=dict(size=11, color='rgb(166, 10, 61)'),
        text=lidl_df[['name', 'address', 'zip', 'district']].apply(lambda row: '<br>'.join(row), axis=1),
        name='Lidl', 
        line=dict(color='black', width=2)
    ))

    #Adding the Aldi points
    fig2.add_trace(go.Scattermapbox(
        lat=aldi_df['lat'],
        lon=aldi_df['lng'],
        mode='markers',
        marker=dict(size=12, color='rgb(224, 152, 33)'),
        text=aldi_df[['name', 'address', 'zip', 'district']].apply(lambda row: '<br>'.join(row), axis=1),
        name='Aldi',
        line=dict(color='black', width=2)
    ))

    #Updating Layout
    fig2.update_layout(
        margin={"r": 0.2, "t": 0.2, "l": 0.2, "b": 0.2},
        title="Store Locations in Munich",
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lng,),
            zoom=10,
        ),
        height=600,
        width=970,
        legend=dict(
            x=0.9,  
            y=0.95,
            font=dict(
                family='sans-serif',
                size=14,
                color='black'
            ),
            bgcolor='rgba(230, 230, 230, 0.8)', 
            bordercolor='black',
            borderwidth=2
        )
    )

    st.plotly_chart(fig2)

    if show_data2:
        #st.subheader(f"{metric} data by district for year {metric_year}:")
        st.subheader("Data Table:")
        st.dataframe(data=df_filtered2)
