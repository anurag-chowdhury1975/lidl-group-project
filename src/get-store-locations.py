import json
import requests
import yaml
import pandas as pd
from math import cos, asin, sqrt, pi

# Function to calculate distance in Km between two latitude/longitude points 
def lat_lon_distance(lat1, lon1, lat2, lon2):
    r = 6371 # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))

def map_dist(zip):
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

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"


# actual api key and other parameters to pass in the search request such as the center location and radius of our search area
# center point for Munich is given in the lat/long below along with the search radius we are using
api_key = gmaps_key
center_lat = 48.137154
center_lng = 11.576124
radius = 15000

# Get Lidl store locations 
# get method of requests module, return response object

# text string on which to search
markets = ["Lidl", "Aldi"]

store_df_list = []

for market in markets:
    req = requests.get(url + "location=" + str(center_lat) + "%2C" + str(center_lng) + "&query=" + market + "%20market&radius=" + str(radius) + "&key=" + gmaps_key)
    
    # json method of response object: json format data -> python format data
    places_json = req.json()
    
    # Json results with our search results from Google maps
    my_result = places_json["results"]

    store_data = []
    for result in my_result:
        name = result.get('name')
        address = result.get('formatted_address')
        zip = result.get('formatted_address').split(', ')[1].split()[0]
        district = map_dist(int(zip))
        lat = result.get('geometry').get('location').get('lat')
        lng = result.get('geometry').get('location').get('lng')
        dist_from_center = lat_lon_distance(center_lat, center_lng, result.get('geometry').get('location').get('lat'), result.get('geometry').get('location').get('lng'))
        rating = result.get('rating')
        num_ratings = result.get('user_ratings_total')
        store_data.append([market, name, address, zip, district, lat, lng, dist_from_center, rating, num_ratings])

    store_df = pd.DataFrame(store_data, columns=['market', 'loc_name', 'address', 'zip', 'district', 'lat', 'lng', 'dist_from_center', 'rating', 'num_ratings'])
    store_df_list.append(store_df)
    
stores_df = pd.concat(store_df_list)
# stores_df[stores_df["market"]=="Aldi"].head()
