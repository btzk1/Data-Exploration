{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# The Hunt For Chinese Restaurants In IPOH\n",
    "\n",
    "Author: Brandon Tan \n",
    "\n",
    "## 1. Introduction \n",
    "Ipoh, home to 800k people is one of the most famous places for food in Malaysia. Every day, many travel a great distance just to taste the famous local cuisine. As a native Ipohrian, on a mission to find all the Chinese restaurants that are located in this beautiful land. This project is mainly an Exploration project and no modeling needed. . \n",
    "\n",
    "\n",
    "## 2. Project Goal\n",
    "My analysis includes the following: \n",
    "- Number of different restaurants\n",
    "- Top 5 Branches of the different restaurants\n",
    "- Top 5 Area with the most Chinese Restaurants\n",
    "- What Chinese Restaurants are located in the Postal Area with most Chinese Restaurants \n",
    "Bonus:\n",
    "- A pie chart demonstrating the Population Percentage by Ethnicity \n",
    "\n",
    "\n",
    "## 3. Project Flow / Sequence\n",
    "1. Data Scrapping (BeautifulSoup)\n",
    "2. Data Cleaning / Wrangling \n",
    "3. Data Exploration / Analytics\n",
    "4. Data Visualization\n",
    "\n",
    "\n",
    "## 4. Data Understanding \n",
    "- Data set: https://postcode.my/location/perak/ipoh/\n",
    "- Description: This dataset contains information such as Location, Postcode and City\n",
    "\n",
    "Venues of different restaurant cruisines\n",
    "\n",
    "- Data set: Foursquare API\n",
    "- Description: Foursqaure API allows us to gain access to venues of different resturants, specifically chinese resturants. \n",
    "\n",
    "Sample Dataset:\n",
    "\n",
    "| Location | Postcode | Latitude\t| Longitude |\n",
    "| --- | --- | --- | --- |\n",
    "| Bangunan Kerajaan Negeri | 30000 | 4.598570 | 101.119880|\n",
    "|Bangunan Perak Darul Ridzuan | 30000|4.605280\t|101.077520|\n",
    "|Bangunan Sri Kinta|\t30000\t|\t4.597900|\t101.080110|\n",
    "|Dei Lok Flat\t|30000\t|4.598570\t|101.119880|\n",
    "|Gunung Cheroh\t|30000|4.597487\t|101.064018|\n",
    "\n",
    "\n",
    "## 5. Tools and Libraries Used\n",
    "\n",
    "| Job |  Tools |Description|\n",
    "| --- | --- | --- |\n",
    "|Collecting Data  | BeautifulSoup |Beautiful Soup is a Python package for parsing HTML and XML documents.  |\n",
    "| Data Cleaning / Wrangling | Pandas  | Pandas is a software library written for the Python programming language for data manipulation and analysis |\n",
    "| Displaying Location on Map | Folium | Folium is a Python library used for visualizing geospatial data. |\n",
    "| Extracting Venue Info | Foursquare API  | Foursqaure API allows us to gain access to venues of different resturants, specifically chinese resturants. |\n",
    "| Visualization | Matplotlib  | Matplotlib is a plotting library for the Python programming language and its numerical mathematics extension NumPy.  |\n",
    "\n",
    "\n",
    "\n",
    "## 6. Findings & Summary\n",
    "1. A total of 6330 postal areas\n",
    "2. 1491 postal areas in Ipoh \n",
    "3. 463 Chinese Resturants \n",
    "4. Top 5 Restaurants are:\n",
    "\n",
    "| Restaurant | Branches |\n",
    "| --- | --- |\n",
    "| Sam Ma Chicken Rice 三妈芽菜滑鸡饭 | 99|\n",
    "|Yum Yum Bak Kut Teh| 97|\n",
    "|Restaurant Shion Mun Lau (常满楼饭店)| 65|\n",
    "|Restoran Fu Lim 富臨海鲜酒家|28|\n",
    "|Mee Tarik Warisan Asli | 27|\n",
    "\n",
    "5. Top5 areas with the most chinese restuirants are \n",
    "\n",
    "| Postcode | Amount |\n",
    "| --- | --- |\n",
    "|31350 |37| \n",
    "|30020 |34|\n",
    "|30000 |25| \n",
    "|30100 |10|\n",
    "|30450 |13|\n",
    "\n",
    "6. The restaurant located in postal area 31350 are found below\n",
    "\n",
    "7. Chinese makes the majority population of Ipoh at 44%\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Importing Libraries"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests \n",
    "import pandas as pd \n",
    "import numpy as np \n",
    "import random \n",
    "from geopy.geocoders import Nominatim \n",
    "from IPython.display import Image \n",
    "from IPython.core.display import HTML \n",
    "from pandas.io.json import json_normalize\n",
    "import folium \n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.cm as cm\n",
    "import matplotlib.colors as colors\n",
    "from bs4 import BeautifulSoup as bs\n",
    "import geocoder\n",
    "from pywaffle import Waffle\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Collecting Postcode Data"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**RETRIVING URL & SCRAPPING DATA**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "page_num = 1\n",
    "contents = []\n",
    "while page_num <= 75:\n",
    "    url = \"https://postcode.my/location/perak/ipoh/?page={page_number}\".format(page_number = page_num)\n",
    "    postcode_my_url = requests.get(url).text\n",
    "    # Read the url with pandas\n",
    "    url_data = bs(postcode_my_url, 'html5')\n",
    "    table = url_data.find('table')\n",
    "    # Scrapping the data\n",
    "    for row in table.find_all('td'):\n",
    "        cell = {}\n",
    "        cell['All_Data'] = row.strong.text[:] \n",
    "        contents.append(cell)\n",
    "    page_num += 1\n",
    "   "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**CLEAN DATA TO BE CONVERTED TO DATAFRAME**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Location \n",
    "p = 0\n",
    "location = []\n",
    "while p < len(contents):\n",
    "    location.append(contents[p].get('All_Data'))\n",
    "    p += 4\n",
    "   \n",
    "# Post Code\n",
    "w = 3\n",
    "post_code = []\n",
    "while w < len(contents):\n",
    "    post_code.append(contents[w].get('All_Data'))\n",
    "    w += 4\n",
    "    \n",
    "# City\n",
    "m = 1\n",
    "city = []\n",
    "while m < len(contents):\n",
    "    city.append(contents[m].get('All_Data'))\n",
    "    m += 4"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**CONVERTING DATA TO DATAFRAME**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convert List of dictionaries to dataframe\n",
    "dic = {}\n",
    "t = 0\n",
    "while t < len(contents):\n",
    "    dic['Location'] = location\n",
    "    dic['Post Code'] = post_code\n",
    "    dic[\"City\"] = city\n",
    "    t += 1"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**SAVING OUR DATA TO A CSV FILE**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "perak_df = pd.DataFrame(dic)\n",
    "perak_df.head(10)\n",
    "perak_df.to_csv('Perak_Postcodes.csv')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration\n",
    "Now that we have collected our data on all of the postcodes and areas of Perak, it is time to explore our data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Location</th>\n",
       "      <th>Postcode</th>\n",
       "      <th>City</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Bangunan Kerajaan Negeri</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Bangunan Perak Darul Ridzuan</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Bangunan Sri Kinta</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Dei Lok Flat</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Gunung Cheroh</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6325</th>\n",
       "      <td>PPRT Sejagop</td>\n",
       "      <td>36810</td>\n",
       "      <td>Kampung Gajah</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6326</th>\n",
       "      <td>PPRT Sungai Ranggam</td>\n",
       "      <td>36810</td>\n",
       "      <td>Kampung Gajah</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6327</th>\n",
       "      <td>Ranggam Estate</td>\n",
       "      <td>36810</td>\n",
       "      <td>Kampung Gajah</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6328</th>\n",
       "      <td>Sungai Kabong</td>\n",
       "      <td>36810</td>\n",
       "      <td>Kampung Gajah</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6329</th>\n",
       "      <td>Sungai Renggam</td>\n",
       "      <td>36810</td>\n",
       "      <td>Kampung Gajah</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>6330 rows × 3 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                          Location  Postcode           City\n",
       "0         Bangunan Kerajaan Negeri     30000           Ipoh\n",
       "1     Bangunan Perak Darul Ridzuan     30000           Ipoh\n",
       "2               Bangunan Sri Kinta     30000           Ipoh\n",
       "3                     Dei Lok Flat     30000           Ipoh\n",
       "4                    Gunung Cheroh     30000           Ipoh\n",
       "...                            ...       ...            ...\n",
       "6325                  PPRT Sejagop     36810  Kampung Gajah\n",
       "6326           PPRT Sungai Ranggam     36810  Kampung Gajah\n",
       "6327                Ranggam Estate     36810  Kampung Gajah\n",
       "6328                 Sungai Kabong     36810  Kampung Gajah\n",
       "6329                Sungai Renggam     36810  Kampung Gajah\n",
       "\n",
       "[6330 rows x 3 columns]"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df = pd.read_csv(\"Perak_Postcodes.csv\")\n",
    "df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Our raw data contains 6330 rows which we will clean later on. For our project we will only be focusing on \"IPOH\", hence we will remove other cities"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**DATA WRANGLING**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Removing cities that arent Ipoh\n",
    "df = df[df.City == 'Ipoh']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Check for duplicate values\n",
    "df.duplicated().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Location    0\n",
       "Postcode    0\n",
       "City        0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Checking for invalid values\n",
    "df.isna().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Location</th>\n",
       "      <th>Postcode</th>\n",
       "      <th>City</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Bangunan Kerajaan Negeri</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Bangunan Perak Darul Ridzuan</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Bangunan Sri Kinta</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Dei Lok Flat</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Gunung Cheroh</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2078</th>\n",
       "      <td>Lebuhraya Evergreen</td>\n",
       "      <td>31650</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2079</th>\n",
       "      <td>Lebuhraya Pasir Puteh</td>\n",
       "      <td>31650</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2080</th>\n",
       "      <td>Lebuhraya Satu</td>\n",
       "      <td>31650</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2081</th>\n",
       "      <td>Lebuhraya Tebing Tinggi</td>\n",
       "      <td>31650</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2082</th>\n",
       "      <td>Lengkok Bendahara</td>\n",
       "      <td>31650</td>\n",
       "      <td>Ipoh</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>1491 rows × 3 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                          Location  Postcode  City\n",
       "0         Bangunan Kerajaan Negeri     30000  Ipoh\n",
       "1     Bangunan Perak Darul Ridzuan     30000  Ipoh\n",
       "2               Bangunan Sri Kinta     30000  Ipoh\n",
       "3                     Dei Lok Flat     30000  Ipoh\n",
       "4                    Gunung Cheroh     30000  Ipoh\n",
       "...                            ...       ...   ...\n",
       "2078           Lebuhraya Evergreen     31650  Ipoh\n",
       "2079         Lebuhraya Pasir Puteh     31650  Ipoh\n",
       "2080                Lebuhraya Satu     31650  Ipoh\n",
       "2081       Lebuhraya Tebing Tinggi     31650  Ipoh\n",
       "2082             Lengkok Bendahara     31650  Ipoh\n",
       "\n",
       "[1491 rows x 3 columns]"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Checking our new dataframe after filtering\n",
    "df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "From the table we know that there are 1491 different postal areas in Ipoh"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**RETREVING THE LAT & LONG**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Defining function to get Lat and Long\n",
    "def latlong(postalcode):\n",
    "    lat_long_coord = None\n",
    "    while(lat_long_coord is None):\n",
    "        g = geocoder.arcgis('{}, Ipoh, Perak'.format(postalcode))\n",
    "        lat_long_coord = g.latlng\n",
    "    return lat_long_coord"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "location = df['Location']    \n",
    "coordinates = [latlong(location) for location in location.tolist()]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_geo = pd.DataFrame(coordinates, columns=['Latitude', 'Longitude'])\n",
    "df['Latitude'] = df_geo['Latitude']\n",
    "df['Longitude'] = df_geo['Longitude']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = df.dropna()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save lat & Long data to csv\n",
    "df.to_csv('Ipoh_Lat_Long.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Location</th>\n",
       "      <th>Postcode</th>\n",
       "      <th>City</th>\n",
       "      <th>Latitude</th>\n",
       "      <th>Longitude</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Bangunan Kerajaan Negeri</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.598570</td>\n",
       "      <td>101.119880</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Bangunan Perak Darul Ridzuan</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.605280</td>\n",
       "      <td>101.077520</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Bangunan Sri Kinta</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.597900</td>\n",
       "      <td>101.080110</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Dei Lok Flat</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.598570</td>\n",
       "      <td>101.119880</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Gunung Cheroh</td>\n",
       "      <td>30000</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.597487</td>\n",
       "      <td>101.064018</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>994</th>\n",
       "      <td>Taman Cahaya Bercham</td>\n",
       "      <td>31400</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.570382</td>\n",
       "      <td>101.080999</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>995</th>\n",
       "      <td>Taman Cahaya Tasek</td>\n",
       "      <td>31400</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.539574</td>\n",
       "      <td>101.058016</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>996</th>\n",
       "      <td>Taman Canning</td>\n",
       "      <td>31400</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.580136</td>\n",
       "      <td>101.098673</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>997</th>\n",
       "      <td>Taman Cempaka</td>\n",
       "      <td>31400</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.579678</td>\n",
       "      <td>101.076126</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>998</th>\n",
       "      <td>Taman Cempaka Sari</td>\n",
       "      <td>31400</td>\n",
       "      <td>Ipoh</td>\n",
       "      <td>4.581019</td>\n",
       "      <td>101.076348</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>999 rows × 5 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                         Location  Postcode  City  Latitude   Longitude\n",
       "0        Bangunan Kerajaan Negeri     30000  Ipoh  4.598570  101.119880\n",
       "1    Bangunan Perak Darul Ridzuan     30000  Ipoh  4.605280  101.077520\n",
       "2              Bangunan Sri Kinta     30000  Ipoh  4.597900  101.080110\n",
       "3                    Dei Lok Flat     30000  Ipoh  4.598570  101.119880\n",
       "4                   Gunung Cheroh     30000  Ipoh  4.597487  101.064018\n",
       "..                            ...       ...   ...       ...         ...\n",
       "994          Taman Cahaya Bercham     31400  Ipoh  4.570382  101.080999\n",
       "995            Taman Cahaya Tasek     31400  Ipoh  4.539574  101.058016\n",
       "996                 Taman Canning     31400  Ipoh  4.580136  101.098673\n",
       "997                 Taman Cempaka     31400  Ipoh  4.579678  101.076126\n",
       "998            Taman Cempaka Sari     31400  Ipoh  4.581019  101.076348\n",
       "\n",
       "[999 rows x 5 columns]"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# lets look at our newdataframe\n",
    "df = pd.read_csv('Ipoh_Lat_Long.csv')\n",
    "df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**PLOTTING OUR LAT & LONG ON A MAP**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The coordinates of Ipoh are 4.5986817, 101.0900236.\n"
     ]
    }
   ],
   "source": [
    "address = 'Ipoh, Perak'\n",
    "\n",
    "geolocator = Nominatim(user_agent=\"ipoh_explorer\")\n",
    "location = geolocator.geocode(address)\n",
    "latitude = location.latitude\n",
    "longitude = location.longitude\n",
    "print('The coordinates of Ipoh are {}, {}.'.format(latitude, longitude))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Lets visually see what our data point looks like on a map"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
      ],
      "text/plain": [
       "<folium.folium.Map at 0x13b77cdba88>"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "map_ipoh = folium.Map(location=[latitude, longitude], zoom_start=12)\n",
    "for lat, lng, location, postalcode in zip(df['Latitude'], df['Longitude'], df['Location'], df['Postcode']):\n",
    "    label = '{}, {}'.format(location, postalcode)\n",
    "    label = folium.Popup(label, parse_html=True)\n",
    "    folium.CircleMarker(\n",
    "        [lat, lng],\n",
    "        radius=4,\n",
    "        popup=label,\n",
    "        color='blue',\n",
    "        fill=True,\n",
    "        fill_color='#87cefa',\n",
    "        fill_opacity=0.5,\n",
    "        parse_html=False).add_to(map_ipoh)\n",
    "map_ipoh"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The map displays all the postal areas of ipoh. Next we will use connect to the FourSquare API to grab information of all the available Chinese Restaurants in the given postal area in the map"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**GETTING LOCATION OF RESTURANTS**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will now use Four Square API to get restaurant locations around ipoh"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Four Square Credentials\n",
    "CLIENT_ID = '3HA5I1NALIQBX0X2QJAWUTAIJNG4N2GOWJEXWVWFP4FYAO3V'    \n",
    "CLIENT_SECRET = 'HSMUV2PIJJG3RESNP4U53NKWE2XDP0DM3M5FEMPAZFYJAJ5X'\n",
    "VERSION = '20180604'\n",
    "radius = 10000\n",
    "LIMIT = 100"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**DEFININF A FUNCTION TO GET VENUES**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_venues(lat,lng):\n",
    "    # URL link to fetch data from foursquare api\n",
    "    url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(\n",
    "            CLIENT_ID, \n",
    "            CLIENT_SECRET, \n",
    "            VERSION, \n",
    "            lat, \n",
    "            lng, \n",
    "            radius, \n",
    "            LIMIT)\n",
    "    \n",
    "    # Retrieve all data\n",
    "    results = requests.get(url).json()\n",
    "    venue_data=results[\"response\"]['groups'][0]['items']\n",
    "    venue_details=[]\n",
    "    for row in venue_data:\n",
    "        try:\n",
    "            venue_id=row['venue']['id']\n",
    "            venue_name=row['venue']['name']\n",
    "            venue_category=row['venue']['categories'][0]['name']\n",
    "            venue_details.append([venue_id,venue_name,venue_category])\n",
    "        except KeyError:\n",
    "            pass\n",
    "        \n",
    "    column_names=['ID','Name','Category']\n",
    "    df = pd.DataFrame(venue_details,columns=column_names)\n",
    "    return df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**PREPARING NEIGHBOURING LIST THAT CONTAINS RESTAURANTS**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Collect ID, NAME, CATEGORY\n",
    "column_names = ['Location', 'Postcode', 'ID','Name','Latitude','Longitude','Category']\n",
    "rest_ipoh = pd.DataFrame(columns=column_names)\n",
    "count = 1\n",
    "for row in df.values.tolist():\n",
    "    Location, Postcode, City ,Latitude, Longitude = row\n",
    "    venues = get_venues(Latitude,Longitude)\n",
    "    ipoh_resturants = venues[venues['Category']=='Chinese Restaurant']   \n",
    "    #print('(',count,'/',len(df),')','Resturants in '+Location+', '+Postcode+':'+str(len(ipoh_resturants)))\n",
    "    for resturant_detail in ipoh_resturants.values.tolist():\n",
    "        id, name , category = resturant_detail\n",
    "        rest_ipoh = rest_ipoh.append({'Location': Location,\n",
    "                                                'Postcode':Postcode, \n",
    "                                                'ID': id,\n",
    "                                                'Name' : name,\n",
    "                                                'Latitude' : Latitude,\n",
    "                                                'Longitude' : Longitude,\n",
    "                                                'Category' : category\n",
    "                                               }, ignore_index=True)\n",
    "    count+=1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unnamed: 0</th>\n",
       "      <th>Location</th>\n",
       "      <th>Postcode</th>\n",
       "      <th>ID</th>\n",
       "      <th>Name</th>\n",
       "      <th>Latitude</th>\n",
       "      <th>Longitude</th>\n",
       "      <th>Category</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>Bangunan Kerajaan Negeri</td>\n",
       "      <td>30000</td>\n",
       "      <td>590da6fcf62e096687c00303</td>\n",
       "      <td>Sam Ma Chicken Rice 三妈芽菜滑鸡饭</td>\n",
       "      <td>4.59857</td>\n",
       "      <td>101.11988</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>Bangunan Kerajaan Negeri</td>\n",
       "      <td>30000</td>\n",
       "      <td>4dbd3ba26a23e294ba40ecf7</td>\n",
       "      <td>Yum Yum Bak Kut Teh</td>\n",
       "      <td>4.59857</td>\n",
       "      <td>101.11988</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Unnamed: 0                  Location  Postcode                        ID  \\\n",
       "0           0  Bangunan Kerajaan Negeri     30000  590da6fcf62e096687c00303   \n",
       "1           1  Bangunan Kerajaan Negeri     30000  4dbd3ba26a23e294ba40ecf7   \n",
       "\n",
       "                          Name  Latitude  Longitude            Category  \n",
       "0  Sam Ma Chicken Rice 三妈芽菜滑鸡饭   4.59857  101.11988  Chinese Restaurant  \n",
       "1          Yum Yum Bak Kut Teh   4.59857  101.11988  Chinese Restaurant  "
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ipoh_rest_df.head(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save Restaurant Data \n",
    "rest_ipoh.to_csv('Ipoh Chinese Resturants.csv')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# EXPLORING IPOH CHINESE RESTAURANT DATA"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unnamed: 0</th>\n",
       "      <th>Location</th>\n",
       "      <th>Postcode</th>\n",
       "      <th>ID</th>\n",
       "      <th>Name</th>\n",
       "      <th>Latitude</th>\n",
       "      <th>Longitude</th>\n",
       "      <th>Category</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>Bangunan Kerajaan Negeri</td>\n",
       "      <td>30000</td>\n",
       "      <td>590da6fcf62e096687c00303</td>\n",
       "      <td>Sam Ma Chicken Rice 三妈芽菜滑鸡饭</td>\n",
       "      <td>4.598570</td>\n",
       "      <td>101.119880</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>Bangunan Kerajaan Negeri</td>\n",
       "      <td>30000</td>\n",
       "      <td>4dbd3ba26a23e294ba40ecf7</td>\n",
       "      <td>Yum Yum Bak Kut Teh</td>\n",
       "      <td>4.598570</td>\n",
       "      <td>101.119880</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>Bangunan Kerajaan Negeri</td>\n",
       "      <td>30000</td>\n",
       "      <td>4ca2cef1f832a1cde76a98e5</td>\n",
       "      <td>Restaurant Shion Mun Lau (常满楼饭店)</td>\n",
       "      <td>4.598570</td>\n",
       "      <td>101.119880</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>Bangunan Perak Darul Ridzuan</td>\n",
       "      <td>30000</td>\n",
       "      <td>4dbd3ba26a23e294ba40ecf7</td>\n",
       "      <td>Yum Yum Bak Kut Teh</td>\n",
       "      <td>4.605280</td>\n",
       "      <td>101.077520</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4</td>\n",
       "      <td>Bangunan Perak Darul Ridzuan</td>\n",
       "      <td>30000</td>\n",
       "      <td>4bfa71c15317a593409d027f</td>\n",
       "      <td>Restaurant Chap Heng</td>\n",
       "      <td>4.605280</td>\n",
       "      <td>101.077520</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4632</th>\n",
       "      <td>4632</td>\n",
       "      <td>Jalan Edward Morera</td>\n",
       "      <td>31400</td>\n",
       "      <td>4cff1559ba1da1cd6f988128</td>\n",
       "      <td>南茶餐室</td>\n",
       "      <td>4.575118</td>\n",
       "      <td>101.080185</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4633</th>\n",
       "      <td>4633</td>\n",
       "      <td>Jalan endah</td>\n",
       "      <td>31400</td>\n",
       "      <td>4dbd3ba26a23e294ba40ecf7</td>\n",
       "      <td>Yum Yum Bak Kut Teh</td>\n",
       "      <td>4.583531</td>\n",
       "      <td>101.081896</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4634</th>\n",
       "      <td>4634</td>\n",
       "      <td>Jalan endah</td>\n",
       "      <td>31400</td>\n",
       "      <td>590da6fcf62e096687c00303</td>\n",
       "      <td>Sam Ma Chicken Rice 三妈芽菜滑鸡饭</td>\n",
       "      <td>4.583531</td>\n",
       "      <td>101.081896</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4635</th>\n",
       "      <td>4635</td>\n",
       "      <td>Jalan endah</td>\n",
       "      <td>31400</td>\n",
       "      <td>57e3660bcd10989c7d49e369</td>\n",
       "      <td>Mee Tarik Warisan Asli</td>\n",
       "      <td>4.583531</td>\n",
       "      <td>101.081896</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4636</th>\n",
       "      <td>4636</td>\n",
       "      <td>Jalan endah</td>\n",
       "      <td>31400</td>\n",
       "      <td>4dcdd9dcb0fb25f6e335ba01</td>\n",
       "      <td>Kopitiam Chee Kong</td>\n",
       "      <td>4.583531</td>\n",
       "      <td>101.081896</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>4637 rows × 8 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "      Unnamed: 0                      Location  Postcode  \\\n",
       "0              0      Bangunan Kerajaan Negeri     30000   \n",
       "1              1      Bangunan Kerajaan Negeri     30000   \n",
       "2              2      Bangunan Kerajaan Negeri     30000   \n",
       "3              3  Bangunan Perak Darul Ridzuan     30000   \n",
       "4              4  Bangunan Perak Darul Ridzuan     30000   \n",
       "...          ...                           ...       ...   \n",
       "4632        4632           Jalan Edward Morera     31400   \n",
       "4633        4633                   Jalan endah     31400   \n",
       "4634        4634                   Jalan endah     31400   \n",
       "4635        4635                   Jalan endah     31400   \n",
       "4636        4636                   Jalan endah     31400   \n",
       "\n",
       "                            ID                              Name  Latitude  \\\n",
       "0     590da6fcf62e096687c00303       Sam Ma Chicken Rice 三妈芽菜滑鸡饭  4.598570   \n",
       "1     4dbd3ba26a23e294ba40ecf7               Yum Yum Bak Kut Teh  4.598570   \n",
       "2     4ca2cef1f832a1cde76a98e5  Restaurant Shion Mun Lau (常满楼饭店)  4.598570   \n",
       "3     4dbd3ba26a23e294ba40ecf7               Yum Yum Bak Kut Teh  4.605280   \n",
       "4     4bfa71c15317a593409d027f              Restaurant Chap Heng  4.605280   \n",
       "...                        ...                               ...       ...   \n",
       "4632  4cff1559ba1da1cd6f988128                              南茶餐室  4.575118   \n",
       "4633  4dbd3ba26a23e294ba40ecf7               Yum Yum Bak Kut Teh  4.583531   \n",
       "4634  590da6fcf62e096687c00303       Sam Ma Chicken Rice 三妈芽菜滑鸡饭  4.583531   \n",
       "4635  57e3660bcd10989c7d49e369            Mee Tarik Warisan Asli  4.583531   \n",
       "4636  4dcdd9dcb0fb25f6e335ba01                Kopitiam Chee Kong  4.583531   \n",
       "\n",
       "       Longitude            Category  \n",
       "0     101.119880  Chinese Restaurant  \n",
       "1     101.119880  Chinese Restaurant  \n",
       "2     101.119880  Chinese Restaurant  \n",
       "3     101.077520  Chinese Restaurant  \n",
       "4     101.077520  Chinese Restaurant  \n",
       "...          ...                 ...  \n",
       "4632  101.080185  Chinese Restaurant  \n",
       "4633  101.081896  Chinese Restaurant  \n",
       "4634  101.081896  Chinese Restaurant  \n",
       "4635  101.081896  Chinese Restaurant  \n",
       "4636  101.081896  Chinese Restaurant  \n",
       "\n",
       "[4637 rows x 8 columns]"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ipoh_rest_df = pd.read_csv('Ipoh Chinese Resturants.csv')\n",
    "ipoh_rest_df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "After succesfully retrieving all the Chinese Restaurant names in our given postal area, its time to clean and explore our data\n",
    "\n",
    "For our Analysis we will be exploring: \n",
    "- Number of different restaurants\n",
    "- Top 5 Branches of the different restaurants\n",
    "- Top 5 Area with the most Chinese Restaurants\n",
    "- What Chinese Restaurants are located in the Postal Area with most Chinese Restaurants \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**NUMBER OF DIFFERENT RESTAURANTS**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['Sam Ma Chicken Rice 三妈芽菜滑鸡饭', 'Yum Yum Bak Kut Teh',\n",
       "       'Restaurant Shion Mun Lau (常满楼饭店)', 'Restaurant Chap Heng',\n",
       "       'Restoran Fu Lim 富臨海鲜酒家', '来发茶餐室',\n",
       "       'Famous Jelapang Road Side Laksa And Fruit Rojak', '文记饭店', '龙记肉骨茶',\n",
       "       'Cashier Market', '新美源海鮮飯店', 'Yew Lee 有利茶餐室',\n",
       "       'Kedai Kopi Kok Beng Chicken Rice', '福满楼海鲜粥', '月球茶餐室',\n",
       "       'Mee Tarik Warisan Asli', 'Kopitiam Chee Kong', '志光茶室', '喜城茶餐室',\n",
       "       '张洲茶餐室', 'Falim 鱼旦仔粉饭档', 'Restoran Soo Har Yee 苏乞儿海鲜饭店',\n",
       "       'Fei Bo Snow Beer East 肥波雪花啤酒', 'Restoran Fok Heng',\n",
       "       'Restoran Fook Kee 福记', '南茶餐室', 'Kedai Kopi You Like It 好锺意茶餐室',\n",
       "       '豐滿樓 Phongmun Restaurant', '东京海鲜饭店',\n",
       "       'Kedai Makanan Lok Fatt 68家乡饭店', 'Kheng Hiong',\n",
       "       'Restoran Yin Fei 晏菲茶餐室', 'Restaurant Choy Pin (萍萍茶餐室)', '江沙牛肉面',\n",
       "       '利民加地小食中心', '钻石咖喱粉', 'Hong Kong Oil Chicken & Roast Duck',\n",
       "       '江沙路茶餐室', 'Restoran Ming Feong', 'Rainbow Seafood Restaurant',\n",
       "       'Restoran Wong Sheng 旺盛海鲜饭店', '食之味', 'Sizzling Wok',\n",
       "       'Hou Yi Lou Restaurant', '南興隆海鮮飯店 Nam Hing Loong Restaurant',\n",
       "       '园满小食店', '古樓茶室', 'Restaurant Mee Fong', 'Serdang易记海鲜档(炒粥)',\n",
       "       'Restoran Bie You Tian 别有天海鲜 (咖哩山猪肉)', 'Sin Aik Kee Restaurant',\n",
       "       '天虹海鲜酒家', 'KFG Claypot Chicken Rice', 'Restaurant Michelin Star',\n",
       "       '群華海鮮圓酒家', '新一色茶餐室 Restoran Sin Ek Sek',\n",
       "       'Kampung Koh Corner Mee Stall', 'Amu Coconut Villa Restaurant',\n",
       "       '新汉商酒楼 Restoran Sun Hon Siong', 'Restoran Ah Hing', '富强板面'],\n",
       "      dtype=object)"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Lets check number of unique restaurants in Ipoh \n",
    "ipoh_rest_df['Name'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Lets drop duplicate postcodes to see how many restaurant branches \n",
    "ipoh_rest_df = ipoh_rest_df.drop_duplicates(subset=['Postcode', 'Name'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**BRANCHES OF THE DIFFERENT RESTAURANTS**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Sam Ma Chicken Rice 三妈芽菜滑鸡饭          99\n",
       "Yum Yum Bak Kut Teh                  97\n",
       "Restaurant Shion Mun Lau (常满楼饭店)     65\n",
       "Restoran Fu Lim 富臨海鲜酒家               28\n",
       "Mee Tarik Warisan Asli               27\n",
       "                                     ..\n",
       "Restoran Soo Har Yee 苏乞儿海鲜饭店          1\n",
       "志光茶室                                  1\n",
       "南興隆海鮮飯店 Nam Hing Loong Restaurant     1\n",
       "月球茶餐室                                 1\n",
       "食之味                                   1\n",
       "Name: Name, Length: 61, dtype: int64"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ipoh_rest_df['Name'].value_counts()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "As we can see, Sam Ma Chicken Rice *三妈芽菜滑鸡饭*  and *Yum Yum Bak Kut Teh* have locations at 99 and 97 diffent postal areas."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a new dataframe for our top 5\n",
    "data = {'Restaurants':['Sam Ma Chicken Rice 三妈芽菜滑鸡饭','Yum Yum Bak Kut Teh', 'Restaurant Shion Mun Lau (常满楼饭店)',\n",
    "                      'Restoran Fu Lim 富臨海鲜酒家', 'Mee Tarik Warisan Asli'], 'Branches': [99,97,65,28,27]}\n",
    "df_top5_branch = pd.DataFrame(data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Restaurants</th>\n",
       "      <th>Branches</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Sam Ma Chicken Rice 三妈芽菜滑鸡饭</td>\n",
       "      <td>99</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Yum Yum Bak Kut Teh</td>\n",
       "      <td>97</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Restaurant Shion Mun Lau (常满楼饭店)</td>\n",
       "      <td>65</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Restoran Fu Lim 富臨海鲜酒家</td>\n",
       "      <td>28</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Mee Tarik Warisan Asli</td>\n",
       "      <td>27</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                        Restaurants  Branches\n",
       "0       Sam Ma Chicken Rice 三妈芽菜滑鸡饭        99\n",
       "1               Yum Yum Bak Kut Teh        97\n",
       "2  Restaurant Shion Mun Lau (常满楼饭店)        65\n",
       "3            Restoran Fu Lim 富臨海鲜酒家        28\n",
       "4            Mee Tarik Warisan Asli        27"
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df_top5_branch"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now lets plot it on a Waffle Chart"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Waffle size 2160x1440 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.rcParams[\"figure.figsize\"] = [30, 20]\n",
    "plt.rcParams[\"figure.autolayout\"] = True\n",
    "fig = plt.figure(\n",
    "   FigureClass=Waffle,\n",
    "   rows=5,\n",
    "   values=df_top5_branch.Branches,\n",
    "   labels=list(df_top5_branch.Restaurants)\n",
    ")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**TOP 5 AREA WITH THE MOST CHINESE RESTAURANTS**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "31350    37\n",
       "30020    34\n",
       "30000    25\n",
       "30100    20\n",
       "30450    13\n",
       "         ..\n",
       "30596     3\n",
       "30902     2\n",
       "30546     2\n",
       "30500     1\n",
       "30628     1\n",
       "Name: Postcode, Length: 104, dtype: int64"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# We First find the postcodes that has occured most of the time in our dataframe\n",
    "ipoh_rest_df['Postcode'].value_counts()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can see postal areas where there are most Chinese Restaurants are 31350, 30020, 30000, 30100, 30450"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now lets visualize them in a chart "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Select only from the \n",
    "top5_df = ipoh_rest_df.loc[ipoh_rest_df['Postcode'].isin([31350,30020,30000,30100,30450])]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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qhW++uorrFq1ymDvNU9KPVakXEL8C/soIiIiIiIyYNCgQfj6668xfPhwo+8cmqPye7CTiIiIiIgeCwb1RERERERmjkE9EREREZGZY1BPRERERGTm+KIsEREREZGZY0s9EREREZGZY1BPRERERGTmGNQTEREREZk5BvVERERERGaOQT0RERERkZljUE9EREREZOYY1BMRERERmTkG9UREREREZo5BPRERERGRmWNQT0RERERk5hjUExERERGZOQb1RERERERmjkE9EREREZGZY1BPRERERGTmGNQTEREREZk5BvVERERERGaOQT0RERERkZljUE9EREREZOYY1BMRERERmTkG9UREREREZo5BPRERERGRmWNQT0RERERk5hjUExERERGZOQb1RERERERmjkE9EREREZGZY1BPRERERGTmGNQTEREREZk5BvVERERERGaOQT0RERERkZljUE9EREREZOYY1BMRERERmTnLii7Ak0CSpIouAhERERGVgRCiootQoRjU/09lPxGIiIiIzBUbaPn4DRERERGR2WNQT0RERERk5hjUExERERGZOQb1RERERERmjkE9EREREZGZY1BPRERERGTmGNQTEREREZk5BvVERERERGaOQT0RERERkZljUE9EREREZOYY1BMRERERmTkG9UREREREZo5BPRERERGRmWNQT0RERERk5iwrugBERERE/xbe03ZUdBEqTOLcbhVdhEqNLfVERERERGaOQT0RERERkZljUE9EREREZOYY1BMRERERmTkG9UREREREZo5BPRERERGRmWNQT0RERERk5hjUExERERGZOQb1RERERERmjkE9EREREZGZY1BPRERERGTmGNQTEREREZk5BvVERERERGbObIL6cePGwdPTE46OjqhVqxbGjx+P7OxsAEBwcDC0Wi3s7e2Vv2vXrlVwiYmIiIiIHg+zCerfeOMNxMfHIz09HbGxsTh9+jQiIyOV+fPmzUNGRobyV7NmzQosLRERERHR42NZ0QUorgYNGuh91mg0OHfuXAWVhoiIiIjoyWE2LfUAMHfuXDg4OMDNzQ2nT5/GuHHjlHkRERFwdXVFQEAA1qxZYzKdsLAwSJKk/BERERERmTNJCCEquhAl9ffff+Prr7/GqFGj4OHhgV9++QUNGzaEnZ0d9u3bh379+mH16tV48cUXi5WeJEkww91ARERETxjvaTsquggVJnFutwrLm7GcmbXUyxo0aIAmTZpg6NChAICgoCA4OTnBysoKnTt3xsiRI7Fhw4aKLSQRERER0WNilkE9AOTk5Bh9pl6jMdvNIiIiIiIqMbOIfjMyMvD5558jNTUVQgjExcUhIiICnTt3RmpqKn744QdkZmYiLy8PMTExWL58Ofr06VPRxSYiIiIieizMIqiXJAlr165FvXr14ODggF69eqFbt25YvHgxcnJyEB4ejurVq8PFxQUTJkzAhx9+iL59+1Z0sYmIiIiIHguz6NJSp9Nhz549BufZ2dnh6NGjj7lERERERERPDrNoqSciIiIiIuMY1BMRERERmTmzePyG6N+msvZjXJF9GBMREf2bsaWeiIiIiMjMMagnIiIiIjJzDOqJiIiIiMwcg3oiIiIiIjPHoJ6IiIiIyMwxqCciIiIiMnMM6omIiIiIzByDeiIiIiIiM8egnoiIiIjIzD2WoD4rKwvHjx/H77///jiyIyIiIiKqVFQN6r/44gt069YNd+7cUab99ddfqF+/Plq2bImAgACEhITgwYMHamZLRERERFSpqRrUr1y5Ejdv3oSLi4sy7a233sKVK1cwbNgwdO/eHfv27cPHH3+sZrZERERERJWaqkH92bNnERAQoHxOSUnBvn37MHLkSKxYsQLfffcdWrVqha+++krNbImIiIiIKjVVg/rU1FRUrVpV+Xzw4EEAwEsvvaRMa9WqFRITE9XMloiIiIioUlM1qHd3d8elS5eUz7t374ZWq0VQUJAy7cGDB8jPz1czWyIiIiKiSs1SzcSCgoKwdetW7NixA7a2tli3bh1CQkKg1WqVZc6fPw9PT081syUiIiIiqtRUbamfOXMmAKBnz54ICQlBXl4ewsPDlfm3b9/Gvn370Lp1azWzJSIiIiKq1FRtqW/QoAH++usvbNmyBQDQvXt31KlTR5mfkJCAUaNG4eWXX1YzWyIiIiKiSk3VoB4APDw8MG7cOIPzmjVrhmbNmqmdJRERERFRpabq4zd169bF0qVLTS7z8ccfo169empmS0RERERUqaka1CcmJiI1NdXkMqmpqezSkoiIiIhIRaoG9cVx/fp12NnZPe5siYiIiIj+tcr8TP2sWbP0Ph84cMDgcnl5ebh27RrWrVsHf3//smZLRERERET/U+agPiwsTPlfkiQcOHDA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iIiIzJrqQb2sWbNmaNasWXklT0RERERE/1NuQX1hcXFx+PHHH6HVajFgwABUrVr1cWRLRERERFQpqPqi7NSpU+Hk5IQ7d+4o07Zt24bmzZtj6tSpGD9+PJo0aYJr166pmS0RERERUaWmalC/a9cuBAUF6fVOM23aNDg6OuLLL7/EggULkJKSgsjISDWzJSIiIiKq1FQN6i9fvgxfX1/l8/nz5xEfH48JEyZg4MCBmDhxInr06IGdO3eqmS0RERERUaWmalB///592NnZKZ8PHDgASZLQtWtXZZqvry+uXLmiZrZERERERJWaqkG9p6cn4uLilM/bt2+Hq6srmjRpoky7desWdDqdmtkSEREREVVqqvZ+07NnTyxatAhvv/02bG1tsWPHDoSGhkKSJGWZP//8E3Xq1FEzWyIiIiKiSk3VoH769OnYt28fPvzwQwBAw4YNMXv2bGX+2bNn8fPPP2PKlClqZktEREREVKmpGtS7urri5MmTyiM4DRs2hIWFhTLf2toaW7ZsQfPmzdXMloiIiIioUiuXwaf8/PwMTvf29oa3t3d5ZElEREREVGmVS1B/7do1bNmyBWfOnEFmZiY+++wzAEBKSgoSEhLg5+cHW1vb8siaiIiIiKjSUT2onz9/PmbMmIGcnBwAgCRJSlB/69YtBAUFITo6GiNHjlQ7ayIiIiKiSknVLi3Xrl2LqVOnIjAwEN9//z1Gjx6tN79+/fpo1qwZNm3apGa2RERERESVmqot9YsWLYKPjw9iYmKg1Wpx/PjxIss0atQIMTExamZLRERERFSpqdpS/+eff6JLly7QarVGl3F3d0dycrKa2RIRERERVWqqBvVarRZZWVkml7l8+TKcnJzUzJaIiIiIqFJTNahv2rQpdu3ahezsbIPzb9++jR9//BEtW7ZUM1siIiIiokpN1aB+0qRJSExMxAsvvIBz587pzYuNjUWPHj2QmpqKiRMnqpktEREREVGlpuqLsl27dkVkZCSmT5+O+vXrw9KyIHk7OztkZWVBkiRERkaiffv2amZLRERERFSpqd5P/eTJk9G5c2csX74cx48fx507d+Dg4IDAwECMHDkSAQEBamdJRERERFSplcuIsn5+foiKiiqPpImIiIiI6CGqPlNPRERERESPX7m01P/888/47bffkJqairy8vCLzJen/2rv3uKrqfP/j781F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2rXy8/NTSEiILly44OkyYTLWK7ema/977tq1q1JSUvTUU09JklavXq233nqLkFfHXNvz3r1769FHH9WLL74oSfrv//5vrVu3Tlu2bPFkiahlhHqLYJ1662nQoIHOnz/ven/58mU98cQTqqys1IcffqiIiAhCfR3EeuXWFBoa6vozPDIyUidPnpS/v7+kKzdTRkZG6vvvv/dkiTDZtT2PiorS0aNHXQtf/PDDD2ratKkKCws9WSJqGdNvLIJ16q0nJCREp0+fdr2vV6+e1q5dK39/f/Xt29f17wHqFtYrtyaHw6ENGzZo/fr18vX1rbJ2udPprDL1DnWD0+nU3r17tWfPHvn5+VVZ7cbX11fl5eUerA6eQKi3iPfee0+NGzdWly5d5O/vr9DQUNWrV08PPfSQGjVqpPfee8/TJcJkiYmJWrlyZZVt/v7+WrNmjQIDA/kDv45auHChvvrqK0VHR6tZs2aKj49XbGysoqOj9dVXXykzM9PTJaIGREZG6oUXXtCECRN01113adeuXa5927dvV8uWLT1YHWpCWVmZEhISlJCQoNOnTysnJ8e1b8+ePYqJifFgdfAEpt9YDOvUW0dhYaFKS0vVokWLavscDodycnK4aluHsV45rjp+/LhKS0vVpk0bT5eCWlJQUKDCwkL16NHD06WgFhHqAQCoo7799ltFRkbKZrN5uhQANYzpNxbCOvXWQ89xLYfDoVGjRnm6DNSiDh06VLu/AnXH559/rqVLl6qkpEQVFRWaOXOmRo4cqVWrVnm6NHgAV+otYvr06VqwYIFSU1OVkJCgBg0aqLi4WLm5uZo3b57GjBmjKVOmeLpMmIie46d++OEHBQYGVrmJEnVDx44dr7t93759uvfee+Xn56fdu3fXclWoSQsWLNC0adNks9l09913a9CgQTpz5owqKiq0YsUK/dd//ZeeffZZT5eJWkSotwjWqbceem5NV9epvp7KykrNmzePUF8HhYeHKyEhQSNGjNDV/60bhqGJEycqIyNDYWFhGj58uIerhJnatm2r//u//5NhGIqLi9Onn36qbt26SZI2btyoqVOnXvdp4qi7CPUWwTr11kPPrcnf31/9+/e/bt8rKyu1fPlyQn0ddPbsWaWkpOjcuXN69913XT/MR0dHKz8/X5GRkR6uEGa79lkk9evXV1lZmeveicrKSjVq1EhFRUWe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\n",
      "text/plain": [
       "<Figure size 810x450 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(9,5),dpi= 90,facecolor='w')\n",
    "plt.title('Number of Chinese Resturants for each Postal Area in Ipoh',fontsize= 20,pad=30)\n",
    "plt.xlabel('Location', fontsize=15,)\n",
    "plt.ylabel('No.of Chinese Resturants', fontsize=15)\n",
    "colors = ['#ff9999','#66b3ff','#99ff99','#E2A8FE','#ffcc99']\n",
    "top5_df.groupby('Postcode')['Postcode'].count().plot(kind='bar')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Lets Plot them on a map"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div style=\"width:100%;\"><div style=\"position:relative;width:100%;height:0;padding-bottom:60%;\"><span style=\"color:#565656\">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe src=\"about:blank\" style=\"position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;\" data-html=%3C%21DOCTYPE%20html%3E%0A%3Chead%3E%20%20%20%20%0A%20%20%20%20%3Cmeta%20http-equiv%3D%22content-type%22%20content%3D%22text/html%3B%20charset%3DUTF-8%22%20/%3E%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%3Cscript%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20L_NO_TOUCH%20%3D%20false%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20L_DISABLE_3D%20%3D%20false%3B%0A%20%20%20%20%20%20%20%20%3C/script%3E%0A%20%20%20%20%0A%20%20%20%20%3Cstyle%3Ehtml%2C%20body%20%7Bwidth%3A%20100%25%3Bheight%3A%20100%25%3Bmargin%3A%200%3Bpadding%3A%200%3B%7D%3C/style%3E%0A%20%20%20%20%3Cstyle%3E%23map%20%7Bposition%3Aabsolute%3Btop%3A0%3Bbottom%3A0%3Bright%3A0%3Bleft%3A0%3B%7D%3C/style%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.6.0/dist/leaflet.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//code.jquery.com/jquery-1.12.4.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js%22%3E%3C/script%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.6.0/dist/leaflet.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css%22/%3E%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cmeta%20name%3D%22viewport%22%20content%3D%22width%3Ddevice-width%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20initial-scale%3D1.0%2C%20maximum-scale%3D1.0%2C%20user-scalable%3Dno%22%20/%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cstyle%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%23map_8c0992bb3c7e4768ba5f5de58d473bb9%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20position%3A%20relative%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20width%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20height%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20left%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20top%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C/style%3E%0A%20%20%20%20%20%20%20%20%0A%3C/head%3E%0A%3Cbody%3E%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cdiv%20class%3D%22folium-map%22%20id%3D%22map_8c0992bb3c7e4768ba5f5de58d473bb9%22%20%3E%3C/div%3E%0A%20%20%20%20%20%20%20%20%0A%3C/body%3E%0A%3Cscript%3E%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20map_8c0992bb3c7e4768ba5f5de58d473bb9%20%3D%20L.map%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22map_8c0992bb3c7e4768ba5f5de58d473bb9%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20center%3A%20%5B4.5986817%2C%20101.0900236%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20crs%3A%20L.CRS.EPSG3857%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20zoom%3A%2012%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20zoomControl%3A%20true%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20preferCanvas%3A%20false%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20tile_layer_c533a6f48af04bddbbc84a687464b502%20%3D%20L.tileLayer%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22https%3A//%7Bs%7D.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22attribution%22%3A%20%22Data%20by%20%5Cu0026copy%3B%20%5Cu003ca%20href%3D%5C%22http%3A//openstreetmap.org%5C%22%5Cu003eOpenStreetMap%5Cu003c/a%5Cu003e%2C%20under%20%5Cu003ca%20href%3D%5C%22http%3A//www.openstreetmap.org/copyright%5C%22%5Cu003eODbL%5Cu003c/a%5Cu003e.%22%2C%20%22detectRetina%22%3A%20false%2C%20%22maxNativeZoom%22%3A%2018%2C%20%22maxZoom%22%3A%2018%2C%20%22minZoom%22%3A%200%2C%20%22noWrap%22%3A%20false%2C%20%22opacity%22%3A%201%2C%20%22subdomains%22%3A%20%22abc%22%2C%20%22tms%22%3A%20false%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_52fd2df2fd8e4a4d894e65b1287e6f48%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_863e40f9c16c400592d7d00a53156603%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_a7bb801f1dd048628c9c4fbfd38521d5%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_a7bb801f1dd048628c9c4fbfd38521d5%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESam%20Ma%20Chicken%20Rice%20%E4%B8%89%E5%A6%88%E8%8A%BD%E8%8F%9C%E6%BB%91%E9%B8%A1%E9%A5%AD%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_863e40f9c16c400592d7d00a53156603.setContent%28html_a7bb801f1dd048628c9c4fbfd38521d5%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_52fd2df2fd8e4a4d894e65b1287e6f48.bindPopup%28popup_863e40f9c16c400592d7d00a53156603%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_7d863479aade4aad9f4df1ca3bf4265a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_e6bab150f7d24f06af07c2e4a634f10b%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_84da1f246c344f0394dc1a154ae91a4b%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_84da1f246c344f0394dc1a154ae91a4b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EYum%20Yum%20Bak%20Kut%20Teh%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_e6bab150f7d24f06af07c2e4a634f10b.setContent%28html_84da1f246c344f0394dc1a154ae91a4b%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_7d863479aade4aad9f4df1ca3bf4265a.bindPopup%28popup_e6bab150f7d24f06af07c2e4a634f10b%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_358006e8336e42148f67a4c4a0257dcf%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_e6a8d586277b435381acde79ce5f2f95%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_932ddd779e2949dbb0f105c216187152%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_932ddd779e2949dbb0f105c216187152%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Shion%20Mun%20Lau%20%28%E5%B8%B8%E6%BB%A1%E6%A5%BC%E9%A5%AD%E5%BA%97%29%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_e6a8d586277b435381acde79ce5f2f95.setContent%28html_932ddd779e2949dbb0f105c216187152%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_358006e8336e42148f67a4c4a0257dcf.bindPopup%28popup_e6a8d586277b435381acde79ce5f2f95%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_04bed00fc574441ba5ca6365398ee6c8%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.6052800000000005%2C%20101.07752%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_ecbe659f579045afb93b94215800baa8%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_ca37489eca5a4a29adf7cf6f15d8a358%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_ca37489eca5a4a29adf7cf6f15d8a358%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Chap%20Heng%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_ecbe659f579045afb93b94215800baa8.setContent%28html_ca37489eca5a4a29adf7cf6f15d8a358%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_04bed00fc574441ba5ca6365398ee6c8.bindPopup%28popup_ecbe659f579045afb93b94215800baa8%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6bb94a693e2d41fca8c1353581987a11%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.6052800000000005%2C%20101.07752%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_2fa8854c60ea45b48f2ffd71266d0bfb%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_dff37d83e45d4103a3be3a761dfe97e2%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_dff37d83e45d4103a3be3a761dfe97e2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Fu%20Lim%20%E5%AF%8C%E8%87%A8%E6%B5%B7%E9%B2%9C%E9%85%92%E5%AE%B6%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_2fa8854c60ea45b48f2ffd71266d0bfb.setContent%28html_dff37d83e45d4103a3be3a761dfe97e2%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_6bb94a693e2d41fca8c1353581987a11.bindPopup%28popup_2fa8854c60ea45b48f2ffd71266d0bfb%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_12529e39234f4b3ababbfff7290ab490%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.6052800000000005%2C%20101.07752%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_056ba675338e40928f7f6f35e6c628ef%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d1d64ce98f8c451fb25ed85e2dc419c0%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_d1d64ce98f8c451fb25ed85e2dc419c0%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%9D%A5%E5%8F%91%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_056ba675338e40928f7f6f35e6c628ef.setContent%28html_d1d64ce98f8c451fb25ed85e2dc419c0%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_12529e39234f4b3ababbfff7290ab490.bindPopup%28popup_056ba675338e40928f7f6f35e6c628ef%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5e22626f71a14262adcc0c7ed8bc8284%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.6052800000000005%2C%20101.07752%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_d400712f7a5540e8a247aa718f6114e1%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c7252f6a037648a0bfae3a97077310f3%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_c7252f6a037648a0bfae3a97077310f3%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFamous%20Jelapang%20Road%20Side%20Laksa%20And%20Fruit%20Rojak%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_d400712f7a5540e8a247aa718f6114e1.setContent%28html_c7252f6a037648a0bfae3a97077310f3%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_5e22626f71a14262adcc0c7ed8bc8284.bindPopup%28popup_d400712f7a5540e8a247aa718f6114e1%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6dbe280c23de41d782721930d0796005%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.597486729%2C%20101.0640176%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_f2fd81c055a649819add6e584bee62c4%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_b53aa20fe8df4fa88a07e46e65494c1c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_b53aa20fe8df4fa88a07e46e65494c1c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%87%E8%AE%B0%E9%A5%AD%E5%BA%97%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_f2fd81c055a649819add6e584bee62c4.setContent%28html_b53aa20fe8df4fa88a07e46e65494c1c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_6dbe280c23de41d782721930d0796005.bindPopup%28popup_f2fd81c055a649819add6e584bee62c4%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5cb7b133805c415b844a28817df9a56b%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.850261271%2C%20100.7395829%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a4cca901cb6b486694eb4c412e42ec49%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5d27883be5404a3d9623690d40c418d2%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_5d27883be5404a3d9623690d40c418d2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E9%BE%99%E8%AE%B0%E8%82%89%E9%AA%A8%E8%8C%B6%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a4cca901cb6b486694eb4c412e42ec49.setContent%28html_5d27883be5404a3d9623690d40c418d2%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_5cb7b133805c415b844a28817df9a56b.bindPopup%28popup_a4cca901cb6b486694eb4c412e42ec49%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1d913cc74aa54246b895b5dc2b3043c6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.850261271%2C%20100.7395829%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_532f1a32a45742efae312e24622c3858%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d9075950f2d648efa29aaf4424f0a6e1%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_d9075950f2d648efa29aaf4424f0a6e1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECashier%20Market%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_532f1a32a45742efae312e24622c3858.setContent%28html_d9075950f2d648efa29aaf4424f0a6e1%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1d913cc74aa54246b895b5dc2b3043c6.bindPopup%28popup_532f1a32a45742efae312e24622c3858%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1b5eb2bccf9740d7aa179ed4f71eccc9%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.850261271%2C%20100.7395829%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_aaa528784a6e44b7b295853c4822b53b%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5d5f8a13a91d4b23a1236410ac3ae59d%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_5d5f8a13a91d4b23a1236410ac3ae59d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%B0%E7%BE%8E%E6%BA%90%E6%B5%B7%E9%AE%AE%E9%A3%AF%E5%BA%97%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_aaa528784a6e44b7b295853c4822b53b.setContent%28html_5d5f8a13a91d4b23a1236410ac3ae59d%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1b5eb2bccf9740d7aa179ed4f71eccc9.bindPopup%28popup_aaa528784a6e44b7b295853c4822b53b%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c09b87db31da4cd6baf389b6798178d6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.850261271%2C%20100.7395829%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_c21f5d5a67914022a75f161f5ee2ae73%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9a2a3b353eb747f68d8477a6ecfa9bec%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9a2a3b353eb747f68d8477a6ecfa9bec%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EYew%20Lee%20%E6%9C%89%E5%88%A9%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_c21f5d5a67914022a75f161f5ee2ae73.setContent%28html_9a2a3b353eb747f68d8477a6ecfa9bec%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_c09b87db31da4cd6baf389b6798178d6.bindPopup%28popup_c21f5d5a67914022a75f161f5ee2ae73%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8a0bfb3fb4354fbfa8193028ea908e45%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.850261271%2C%20100.7395829%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_8b88703357654258bf5d1cafd2c2deb3%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c95b4e6e75834b178480d4d7196a5f28%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_c95b4e6e75834b178480d4d7196a5f28%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKedai%20Kopi%20Kok%20Beng%20Chicken%20Rice%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_8b88703357654258bf5d1cafd2c2deb3.setContent%28html_c95b4e6e75834b178480d4d7196a5f28%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_8a0bfb3fb4354fbfa8193028ea908e45.bindPopup%28popup_8b88703357654258bf5d1cafd2c2deb3%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b666ab89045649e2a0d4f6a2d8a12550%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.850261271%2C%20100.7395829%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_cd89e642fd1041428fd34320294c7238%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_89c7e8f52e3b4d80bf4085c05f971f8d%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_89c7e8f52e3b4d80bf4085c05f971f8d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E7%A6%8F%E6%BB%A1%E6%A5%BC%E6%B5%B7%E9%B2%9C%E7%B2%A5%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_cd89e642fd1041428fd34320294c7238.setContent%28html_89c7e8f52e3b4d80bf4085c05f971f8d%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_b666ab89045649e2a0d4f6a2d8a12550.bindPopup%28popup_cd89e642fd1041428fd34320294c7238%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6d12b2b7b7bf4ba5874cbb2620f38e10%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.850261271%2C%20100.7395829%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_3e5d73e933a747dbb336ae451bcf8545%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_2933522808634608bbba1b26dce8738b%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_2933522808634608bbba1b26dce8738b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%9C%88%E7%90%83%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_3e5d73e933a747dbb336ae451bcf8545.setContent%28html_2933522808634608bbba1b26dce8738b%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_6d12b2b7b7bf4ba5874cbb2620f38e10.bindPopup%28popup_3e5d73e933a747dbb336ae451bcf8545%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_522b5070d7dc4bc78266707bccf93d08%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.608799956%2C%20101.080745%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_6177089ba2044f1e94d06edc4d27d3e2%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6b887f5d3bf049bf9b30ac2a2e3e2d68%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_6b887f5d3bf049bf9b30ac2a2e3e2d68%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMee%20Tarik%20Warisan%20Asli%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_6177089ba2044f1e94d06edc4d27d3e2.setContent%28html_6b887f5d3bf049bf9b30ac2a2e3e2d68%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_522b5070d7dc4bc78266707bccf93d08.bindPopup%28popup_6177089ba2044f1e94d06edc4d27d3e2%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1dceeb6d542d4663bc1677daefeb3ee7%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.675460041%2C%20101.1525309%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_dfba915a1ae84304838d8ceea68128b0%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9c23c10e25cf4a05bded277b0211de2e%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9c23c10e25cf4a05bded277b0211de2e%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKopitiam%20Chee%20Kong%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_dfba915a1ae84304838d8ceea68128b0.setContent%28html_9c23c10e25cf4a05bded277b0211de2e%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1dceeb6d542d4663bc1677daefeb3ee7.bindPopup%28popup_dfba915a1ae84304838d8ceea68128b0%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_4ab11b3b18ed4cb5bac4bed6aa18c57a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.675460041%2C%20101.1525309%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_69ce658142994553bade71dd592ec289%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_ce86fd61c3fb468689d49bcd0b90cc6c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_ce86fd61c3fb468689d49bcd0b90cc6c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%BF%97%E5%85%89%E8%8C%B6%E5%AE%A4%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_69ce658142994553bade71dd592ec289.setContent%28html_ce86fd61c3fb468689d49bcd0b90cc6c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_4ab11b3b18ed4cb5bac4bed6aa18c57a.bindPopup%28popup_69ce658142994553bade71dd592ec289%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8e38304171a34dd18a4df7b4c077fb23%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.675460041%2C%20101.1525309%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_da55c4c9f5e043ac99c34f473c60d303%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_8d03d132794c4eb8bb3f7635bf238f9d%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_8d03d132794c4eb8bb3f7635bf238f9d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%96%9C%E5%9F%8E%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_da55c4c9f5e043ac99c34f473c60d303.setContent%28html_8d03d132794c4eb8bb3f7635bf238f9d%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_8e38304171a34dd18a4df7b4c077fb23.bindPopup%28popup_da55c4c9f5e043ac99c34f473c60d303%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_f639ecddcd45456ba7e2ec8926b619d8%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.675460041%2C%20101.1525309%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_79c47d6e57f44561859b025c7d37066d%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_a40273f2751f4936bc8ac4a46f8d46dc%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_a40273f2751f4936bc8ac4a46f8d46dc%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%BC%A0%E6%B4%B2%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_79c47d6e57f44561859b025c7d37066d.setContent%28html_a40273f2751f4936bc8ac4a46f8d46dc%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_f639ecddcd45456ba7e2ec8926b619d8.bindPopup%28popup_79c47d6e57f44561859b025c7d37066d%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_3f37be389f964050945c57d215c5bac7%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.585628572%2C%20101.0755282%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_17c0acff481a4ea29642033ef55c0b9a%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_db1377bd6ebc491cbea3022f8d756b18%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_db1377bd6ebc491cbea3022f8d756b18%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFalim%20%E9%B1%BC%E6%97%A6%E4%BB%94%E7%B2%89%E9%A5%AD%E6%A1%A3%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_17c0acff481a4ea29642033ef55c0b9a.setContent%28html_db1377bd6ebc491cbea3022f8d756b18%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_3f37be389f964050945c57d215c5bac7.bindPopup%28popup_17c0acff481a4ea29642033ef55c0b9a%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1ecf572a9984421ab28252f03efe2afa%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.669974652%2C%20101.1575756%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_42d85ccd5a5d4ea6afdd2d00d9af697a%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_39a2bd15d6764dadb29ed79f087915f9%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_39a2bd15d6764dadb29ed79f087915f9%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Soo%20Har%20Yee%20%E8%8B%8F%E4%B9%9E%E5%84%BF%E6%B5%B7%E9%B2%9C%E9%A5%AD%E5%BA%97%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_42d85ccd5a5d4ea6afdd2d00d9af697a.setContent%28html_39a2bd15d6764dadb29ed79f087915f9%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1ecf572a9984421ab28252f03efe2afa.bindPopup%28popup_42d85ccd5a5d4ea6afdd2d00d9af697a%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_55e05205360241aca8c6d5f393cb0fe2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.669974652%2C%20101.1575756%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_6911c44778c44cb9b7268e390cbec736%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_314b50979cc14d5994628ff051992d47%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_314b50979cc14d5994628ff051992d47%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFei%20Bo%20Snow%20Beer%20East%20%E8%82%A5%E6%B3%A2%E9%9B%AA%E8%8A%B1%E5%95%A4%E9%85%92%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_6911c44778c44cb9b7268e390cbec736.setContent%28html_314b50979cc14d5994628ff051992d47%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_55e05205360241aca8c6d5f393cb0fe2.bindPopup%28popup_6911c44778c44cb9b7268e390cbec736%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5442665f7e8a49ffb35ccd3c77d6ed6e%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.669974652%2C%20101.1575756%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_2f1d926842c94920abcd8b73bf44195a%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1d7c90544df4478b959b4baac2886881%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1d7c90544df4478b959b4baac2886881%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Fok%20Heng%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_2f1d926842c94920abcd8b73bf44195a.setContent%28html_1d7c90544df4478b959b4baac2886881%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_5442665f7e8a49ffb35ccd3c77d6ed6e.bindPopup%28popup_2f1d926842c94920abcd8b73bf44195a%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c1a3cbc422354d099cb85f2544696269%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.718960023%2C%20101.1216808%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_8db1389d297e41d882c0ce076028f071%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f14cdd16f34a47bba86cbdf461ba1b66%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_f14cdd16f34a47bba86cbdf461ba1b66%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Fook%20Kee%20%E7%A6%8F%E8%AE%B0%2C%2030000%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_8db1389d297e41d882c0ce076028f071.setContent%28html_f14cdd16f34a47bba86cbdf461ba1b66%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_c1a3cbc422354d099cb85f2544696269.bindPopup%28popup_8db1389d297e41d882c0ce076028f071%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c6a033f4eb414610b6cf85a78c2944ce%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_5a94c1deeabe4aef936aa4b0071c37c7%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9b21dd900fef42e0a5afd1566b2b3c45%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9b21dd900fef42e0a5afd1566b2b3c45%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESam%20Ma%20Chicken%20Rice%20%E4%B8%89%E5%A6%88%E8%8A%BD%E8%8F%9C%E6%BB%91%E9%B8%A1%E9%A5%AD%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_5a94c1deeabe4aef936aa4b0071c37c7.setContent%28html_9b21dd900fef42e0a5afd1566b2b3c45%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_c6a033f4eb414610b6cf85a78c2944ce.bindPopup%28popup_5a94c1deeabe4aef936aa4b0071c37c7%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1642d55d020447bd9e580476a9827e4d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_9d2e764513d04b378a310ccb5d1b5584%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e1599ccd97624f11a116d352661fdd68%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_e1599ccd97624f11a116d352661fdd68%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EYum%20Yum%20Bak%20Kut%20Teh%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_9d2e764513d04b378a310ccb5d1b5584.setContent%28html_e1599ccd97624f11a116d352661fdd68%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1642d55d020447bd9e580476a9827e4d.bindPopup%28popup_9d2e764513d04b378a310ccb5d1b5584%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8a4e043f97fc42d7b79854d222838b87%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_7157123c4bb8485089fbbf148591f4eb%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_688090cb48dc4d16af491a94e9c34779%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_688090cb48dc4d16af491a94e9c34779%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Shion%20Mun%20Lau%20%28%E5%B8%B8%E6%BB%A1%E6%A5%BC%E9%A5%AD%E5%BA%97%29%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_7157123c4bb8485089fbbf148591f4eb.setContent%28html_688090cb48dc4d16af491a94e9c34779%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_8a4e043f97fc42d7b79854d222838b87.bindPopup%28popup_7157123c4bb8485089fbbf148591f4eb%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_be3bfae2e3a9411586808406d55a5045%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.624064011000001%2C%20101.0689405%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_42a13611f34140e8a054f8969bb65fbd%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_299bc5d8051b4552b56d023239df6bb1%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_299bc5d8051b4552b56d023239df6bb1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFamous%20Jelapang%20Road%20Side%20Laksa%20And%20Fruit%20Rojak%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_42a13611f34140e8a054f8969bb65fbd.setContent%28html_299bc5d8051b4552b56d023239df6bb1%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_be3bfae2e3a9411586808406d55a5045.bindPopup%28popup_42a13611f34140e8a054f8969bb65fbd%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8bc167d2a4b94f87ba649f16f90bfdd4%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.624064011000001%2C%20101.0689405%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_f7fda5162ebb4808a50bd20d61efbe1f%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6a90257b20c34d329a946a61a818704d%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_6a90257b20c34d329a946a61a818704d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Chap%20Heng%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_f7fda5162ebb4808a50bd20d61efbe1f.setContent%28html_6a90257b20c34d329a946a61a818704d%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_8bc167d2a4b94f87ba649f16f90bfdd4.bindPopup%28popup_f7fda5162ebb4808a50bd20d61efbe1f%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_073fd56179bf4cf7870b25e551ab7cbe%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.624064011000001%2C%20101.0689405%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_ee2d8cfddbc3415ba7b177ad70da0323%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_fafd51f993c34c399d04c7750c3ffea8%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_fafd51f993c34c399d04c7750c3ffea8%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMee%20Tarik%20Warisan%20Asli%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_ee2d8cfddbc3415ba7b177ad70da0323.setContent%28html_fafd51f993c34c399d04c7750c3ffea8%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_073fd56179bf4cf7870b25e551ab7cbe.bindPopup%28popup_ee2d8cfddbc3415ba7b177ad70da0323%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_60c2dff4b1734a93bf22e5ae7548c677%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.624064011000001%2C%20101.0689405%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_9ed5a3ad7534468fa5936dd5d4fbdc52%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_ee8775765070437ba6fa41b454405c22%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_ee8775765070437ba6fa41b454405c22%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%9D%A5%E5%8F%91%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_9ed5a3ad7534468fa5936dd5d4fbdc52.setContent%28html_ee8775765070437ba6fa41b454405c22%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_60c2dff4b1734a93bf22e5ae7548c677.bindPopup%28popup_9ed5a3ad7534468fa5936dd5d4fbdc52%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_4a10a28a4fe54334a7b26ccbcd96b380%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.624064011000001%2C%20101.0689405%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_54c2322b92024e84aef76e2332340b0b%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_b3bbda8938ae4faa8472ca603d14dd0a%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_b3bbda8938ae4faa8472ca603d14dd0a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Fu%20Lim%20%E5%AF%8C%E8%87%A8%E6%B5%B7%E9%B2%9C%E9%85%92%E5%AE%B6%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_54c2322b92024e84aef76e2332340b0b.setContent%28html_b3bbda8938ae4faa8472ca603d14dd0a%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_4a10a28a4fe54334a7b26ccbcd96b380.bindPopup%28popup_54c2322b92024e84aef76e2332340b0b%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_af472de0f1094b408194e86ceda17813%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.541879997%2C%20101.07254%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_e0a5112388ec4dc9a9b6e4ba8e83cb1f%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bdd8c16c89f5481fa5aa9cff3ba5be5e%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_bdd8c16c89f5481fa5aa9cff3ba5be5e%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%87%E8%AE%B0%E9%A5%AD%E5%BA%97%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_e0a5112388ec4dc9a9b6e4ba8e83cb1f.setContent%28html_bdd8c16c89f5481fa5aa9cff3ba5be5e%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_af472de0f1094b408194e86ceda17813.bindPopup%28popup_e0a5112388ec4dc9a9b6e4ba8e83cb1f%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_2f5da9eab478470aa85dfe5c00c4db0d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.541879997%2C%20101.07254%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_5c3be6962be046eb879872c84a1c28ed%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d8ba36a3e3ea46f6ad1249c89697c664%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_d8ba36a3e3ea46f6ad1249c89697c664%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKedai%20Kopi%20You%20Like%20It%20%E5%A5%BD%E9%94%BA%E6%84%8F%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_5c3be6962be046eb879872c84a1c28ed.setContent%28html_d8ba36a3e3ea46f6ad1249c89697c664%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_2f5da9eab478470aa85dfe5c00c4db0d.bindPopup%28popup_5c3be6962be046eb879872c84a1c28ed%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_facb13d18a8a432ea603f202c24ea52d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.836930029%2C%20101.0800901%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_1c6288990d1a467d8ef9ad50dfcb63e8%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_762aeeb9b2fb4f3ba0eed327719a7326%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_762aeeb9b2fb4f3ba0eed327719a7326%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E8%B1%90%E6%BB%BF%E6%A8%93%20Phongmun%20Restaurant%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_1c6288990d1a467d8ef9ad50dfcb63e8.setContent%28html_762aeeb9b2fb4f3ba0eed327719a7326%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_facb13d18a8a432ea603f202c24ea52d.bindPopup%28popup_1c6288990d1a467d8ef9ad50dfcb63e8%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e4b744a6f32f41a1ac01f42f87ef7957%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.836930029%2C%20101.0800901%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_3687cb5f23ac4633a5621d148d93ea21%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_09ce6b4f704a490b8d026558f45f698d%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_09ce6b4f704a490b8d026558f45f698d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Fook%20Kee%20%E7%A6%8F%E8%AE%B0%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_3687cb5f23ac4633a5621d148d93ea21.setContent%28html_09ce6b4f704a490b8d026558f45f698d%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_e4b744a6f32f41a1ac01f42f87ef7957.bindPopup%28popup_3687cb5f23ac4633a5621d148d93ea21%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_7c6b99a5191d4caf8a715fcbe46a49cc%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.836930029%2C%20101.0800901%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a3fc32efd0f6455ca46b800292ca7c36%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_908517d6653746319b5d74f5700020f2%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_908517d6653746319b5d74f5700020f2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E4%B8%9C%E4%BA%AC%E6%B5%B7%E9%B2%9C%E9%A5%AD%E5%BA%97%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a3fc32efd0f6455ca46b800292ca7c36.setContent%28html_908517d6653746319b5d74f5700020f2%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_7c6b99a5191d4caf8a715fcbe46a49cc.bindPopup%28popup_a3fc32efd0f6455ca46b800292ca7c36%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b14d7cbf91db49569804adb4d70e5813%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.836930029%2C%20101.0800901%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_407553a2f8fc475fbe1b36cad263179d%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_65448757998f4d13b48a526791dc60ce%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_65448757998f4d13b48a526791dc60ce%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKedai%20Makanan%20Lok%20Fatt%2068%E5%AE%B6%E4%B9%A1%E9%A5%AD%E5%BA%97%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_407553a2f8fc475fbe1b36cad263179d.setContent%28html_65448757998f4d13b48a526791dc60ce%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_b14d7cbf91db49569804adb4d70e5813.bindPopup%28popup_407553a2f8fc475fbe1b36cad263179d%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_19c36cf37b4d4f2c8c1ccee7857744fe%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.639017593%2C%20101.1411014%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_0baa266e37884cd78ed22d2e5bd605ca%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5718ed3af60249b9bf5dd228079aae75%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_5718ed3af60249b9bf5dd228079aae75%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKopitiam%20Chee%20Kong%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_0baa266e37884cd78ed22d2e5bd605ca.setContent%28html_5718ed3af60249b9bf5dd228079aae75%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_19c36cf37b4d4f2c8c1ccee7857744fe.bindPopup%28popup_0baa266e37884cd78ed22d2e5bd605ca%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1257831a10a44fdc87fbcc975c0c84f4%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.4333300000000015%2C%20100.91667%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_1fafa183c30c45c7b7552b415ef4ad14%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9db92da9b9824874885560e4e182101c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9db92da9b9824874885560e4e182101c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKheng%20Hiong%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_1fafa183c30c45c7b7552b415ef4ad14.setContent%28html_9db92da9b9824874885560e4e182101c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1257831a10a44fdc87fbcc975c0c84f4.bindPopup%28popup_1fafa183c30c45c7b7552b415ef4ad14%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_2e0e74d2385449359237d0ee01532ded%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.4333300000000015%2C%20100.91667%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_691763e656694260aee0810b50e52ea6%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f720ce9e8543469b9d9135a1065e22a0%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_f720ce9e8543469b9d9135a1065e22a0%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Yin%20Fei%20%E6%99%8F%E8%8F%B2%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_691763e656694260aee0810b50e52ea6.setContent%28html_f720ce9e8543469b9d9135a1065e22a0%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_2e0e74d2385449359237d0ee01532ded.bindPopup%28popup_691763e656694260aee0810b50e52ea6%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b1d8262942f14e75b3bbf563e233b87f%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.4333300000000015%2C%20100.91667%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_9d58d9134cd84c17897783787bfeda46%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bc30a1ecd18e4888badd7f002e2b71f5%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_bc30a1ecd18e4888badd7f002e2b71f5%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Choy%20Pin%20%28%E8%90%8D%E8%90%8D%E8%8C%B6%E9%A4%90%E5%AE%A4%29%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_9d58d9134cd84c17897783787bfeda46.setContent%28html_bc30a1ecd18e4888badd7f002e2b71f5%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_b1d8262942f14e75b3bbf563e233b87f.bindPopup%28popup_9d58d9134cd84c17897783787bfeda46%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_00004c0492ff4370963781226559d686%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.774618479%2C%20100.9373713%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_ecf25f61ef7342bf8cabf48fc209c6dd%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9f834f7da8744d95977e4304712e6c35%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9f834f7da8744d95977e4304712e6c35%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%B1%9F%E6%B2%99%E7%89%9B%E8%82%89%E9%9D%A2%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_ecf25f61ef7342bf8cabf48fc209c6dd.setContent%28html_9f834f7da8744d95977e4304712e6c35%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_00004c0492ff4370963781226559d686.bindPopup%28popup_ecf25f61ef7342bf8cabf48fc209c6dd%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_eed48d97720a41609238aba7a90bb3f0%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.774618479%2C%20100.9373713%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_116db83e9b0e4de0a26ba8b83a214ac5%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_4cb36366f7974dec98d3531f473a34be%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_4cb36366f7974dec98d3531f473a34be%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%88%A9%E6%B0%91%E5%8A%A0%E5%9C%B0%E5%B0%8F%E9%A3%9F%E4%B8%AD%E5%BF%83%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_116db83e9b0e4de0a26ba8b83a214ac5.setContent%28html_4cb36366f7974dec98d3531f473a34be%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_eed48d97720a41609238aba7a90bb3f0.bindPopup%28popup_116db83e9b0e4de0a26ba8b83a214ac5%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_fc45c4f80a6249c1b6bbbce0c5d8997e%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.57101%2C%20101.05456%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_dbbfcb46f8d34a0fa2ba81b029e670ba%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5d313efe62854b1eb814c4a31d1f6b8f%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_5d313efe62854b1eb814c4a31d1f6b8f%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFalim%20%E9%B1%BC%E6%97%A6%E4%BB%94%E7%B2%89%E9%A5%AD%E6%A1%A3%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_dbbfcb46f8d34a0fa2ba81b029e670ba.setContent%28html_5d313efe62854b1eb814c4a31d1f6b8f%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_fc45c4f80a6249c1b6bbbce0c5d8997e.bindPopup%28popup_dbbfcb46f8d34a0fa2ba81b029e670ba%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b99b9a62d3cb4789a0deb175268ea5a8%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.57101%2C%20101.05456%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_354d88238eeb4614b2f3345bd23c26a7%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_870915040b1046df998a8220d33e4829%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_870915040b1046df998a8220d33e4829%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E9%92%BB%E7%9F%B3%E5%92%96%E5%96%B1%E7%B2%89%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_354d88238eeb4614b2f3345bd23c26a7.setContent%28html_870915040b1046df998a8220d33e4829%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_b99b9a62d3cb4789a0deb175268ea5a8.bindPopup%28popup_354d88238eeb4614b2f3345bd23c26a7%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_75c4eb1b93b54ce7b2a1af2ace346dd4%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.852466567%2C%20100.7148205%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a57f449072994b459ba824eeef1b2ac0%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_8c3bd82835cd4ebbacda6796a3ee22f9%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_8c3bd82835cd4ebbacda6796a3ee22f9%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E9%BE%99%E8%AE%B0%E8%82%89%E9%AA%A8%E8%8C%B6%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a57f449072994b459ba824eeef1b2ac0.setContent%28html_8c3bd82835cd4ebbacda6796a3ee22f9%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_75c4eb1b93b54ce7b2a1af2ace346dd4.bindPopup%28popup_a57f449072994b459ba824eeef1b2ac0%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_19761c3e81624d41bd22661dcda7a393%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.852466567%2C%20100.7148205%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_7a0e348858734b328f7cf6d539199b4b%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_ed1ddf6793ee4ea4927ccdf58e0f8396%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_ed1ddf6793ee4ea4927ccdf58e0f8396%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECashier%20Market%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_7a0e348858734b328f7cf6d539199b4b.setContent%28html_ed1ddf6793ee4ea4927ccdf58e0f8396%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_19761c3e81624d41bd22661dcda7a393.bindPopup%28popup_7a0e348858734b328f7cf6d539199b4b%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_22600e8a90414fa2a801c5731c4303d7%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.852466567%2C%20100.7148205%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_d7279d00d330439d862cf567d97fadf1%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_83079c72b4f94d5294d54ea2a6f4f243%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_83079c72b4f94d5294d54ea2a6f4f243%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%B0%E7%BE%8E%E6%BA%90%E6%B5%B7%E9%AE%AE%E9%A3%AF%E5%BA%97%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_d7279d00d330439d862cf567d97fadf1.setContent%28html_83079c72b4f94d5294d54ea2a6f4f243%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_22600e8a90414fa2a801c5731c4303d7.bindPopup%28popup_d7279d00d330439d862cf567d97fadf1%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9dfc8ec3f8794d02898f8625628addd7%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.852466567%2C%20100.7148205%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a21cff9fa6394c088a3a990b7d3d8d4e%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_84f87c778c5247f8aa70019ef97bbdeb%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_84f87c778c5247f8aa70019ef97bbdeb%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EYew%20Lee%20%E6%9C%89%E5%88%A9%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a21cff9fa6394c088a3a990b7d3d8d4e.setContent%28html_84f87c778c5247f8aa70019ef97bbdeb%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_9dfc8ec3f8794d02898f8625628addd7.bindPopup%28popup_a21cff9fa6394c088a3a990b7d3d8d4e%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_4b3128b9ae364519aba39b9179ac5512%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.852466567%2C%20100.7148205%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_cc964cca480d4a6bb7ff2fec6e5c8815%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1825fbdd20204583863e7b22b2aab36b%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1825fbdd20204583863e7b22b2aab36b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKedai%20Kopi%20Kok%20Beng%20Chicken%20Rice%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_cc964cca480d4a6bb7ff2fec6e5c8815.setContent%28html_1825fbdd20204583863e7b22b2aab36b%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_4b3128b9ae364519aba39b9179ac5512.bindPopup%28popup_cc964cca480d4a6bb7ff2fec6e5c8815%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_2e16f055e19d421a838168d97ccb0452%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.852466567%2C%20100.7148205%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_b0cb0ad3fc674ed6a699a93a4cf2ad2e%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_095e887d7e2142828decf8381942ac18%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_095e887d7e2142828decf8381942ac18%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E7%A6%8F%E6%BB%A1%E6%A5%BC%E6%B5%B7%E9%B2%9C%E7%B2%A5%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_b0cb0ad3fc674ed6a699a93a4cf2ad2e.setContent%28html_095e887d7e2142828decf8381942ac18%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_2e16f055e19d421a838168d97ccb0452.bindPopup%28popup_b0cb0ad3fc674ed6a699a93a4cf2ad2e%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_89604408e5914610914f8a6feabaf476%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.569272493%2C%20101.0829886%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_99748ee617ba4d79a17394f75c5cbf63%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_601d1a187e244287886ee955ca064f94%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_601d1a187e244287886ee955ca064f94%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%8D%97%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_99748ee617ba4d79a17394f75c5cbf63.setContent%28html_601d1a187e244287886ee955ca064f94%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_89604408e5914610914f8a6feabaf476.bindPopup%28popup_99748ee617ba4d79a17394f75c5cbf63%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_f61abf95401048359b92a28e3ddbd700%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.569272493%2C%20101.0829886%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_1966fbf3017342778dc61f99794b15fc%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_0920f87e23c34fb38705b1749ec4549c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_0920f87e23c34fb38705b1749ec4549c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHong%20Kong%20Oil%20Chicken%20%26amp%3B%20Roast%20Duck%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_1966fbf3017342778dc61f99794b15fc.setContent%28html_0920f87e23c34fb38705b1749ec4549c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_f61abf95401048359b92a28e3ddbd700.bindPopup%28popup_1966fbf3017342778dc61f99794b15fc%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_2934e2bd0dcc46fea9be6b2f8e691383%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.569272493%2C%20101.0829886%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_7cf4874467fb4491a85333c7bc5aa9b2%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_09b16520be0940b08be63107b9b1ce43%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_09b16520be0940b08be63107b9b1ce43%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%B1%9F%E6%B2%99%E8%B7%AF%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_7cf4874467fb4491a85333c7bc5aa9b2.setContent%28html_09b16520be0940b08be63107b9b1ce43%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_2934e2bd0dcc46fea9be6b2f8e691383.bindPopup%28popup_7cf4874467fb4491a85333c7bc5aa9b2%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1903bf0c12674cc99f895194d8766ead%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.533146493%2C%20101.0674805%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_7ea80fa83fd346ae822912afe6792d6c%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e364b29a3d99455f951629c619ccc211%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_e364b29a3d99455f951629c619ccc211%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Ming%20Feong%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_7ea80fa83fd346ae822912afe6792d6c.setContent%28html_e364b29a3d99455f951629c619ccc211%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1903bf0c12674cc99f895194d8766ead.bindPopup%28popup_7ea80fa83fd346ae822912afe6792d6c%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c1fe9adc53294e639c961202f0a0476e%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.570957197%2C%20101.0366524%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_3a5e1029b2564e5184b56a06cae3de9f%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_03750c878cb948d9b919d898268e3b2a%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_03750c878cb948d9b919d898268e3b2a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERainbow%20Seafood%20Restaurant%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_3a5e1029b2564e5184b56a06cae3de9f.setContent%28html_03750c878cb948d9b919d898268e3b2a%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_c1fe9adc53294e639c961202f0a0476e.bindPopup%28popup_3a5e1029b2564e5184b56a06cae3de9f%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_40229196adaa4e888876615cb0d30fbf%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.570957197%2C%20101.0366524%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_2f0185bf8b984b4ea4f64f7c59a7804e%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d36b5f2ea0f34387b0f9cd79cbcc7f2f%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_d36b5f2ea0f34387b0f9cd79cbcc7f2f%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Wong%20Sheng%20%E6%97%BA%E7%9B%9B%E6%B5%B7%E9%B2%9C%E9%A5%AD%E5%BA%97%2C%2030020%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_2f0185bf8b984b4ea4f64f7c59a7804e.setContent%28html_d36b5f2ea0f34387b0f9cd79cbcc7f2f%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_40229196adaa4e888876615cb0d30fbf.bindPopup%28popup_2f0185bf8b984b4ea4f64f7c59a7804e%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_cab4470a58aa4bf8b53dc6838fa30031%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.63606285%2C%20101.063452%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_7ff66b8f26744ec28afa454d5fc9b3c7%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_8c6269ef71ee4c58912b7cd33a1f9ff7%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_8c6269ef71ee4c58912b7cd33a1f9ff7%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFamous%20Jelapang%20Road%20Side%20Laksa%20And%20Fruit%20Rojak%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_7ff66b8f26744ec28afa454d5fc9b3c7.setContent%28html_8c6269ef71ee4c58912b7cd33a1f9ff7%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_cab4470a58aa4bf8b53dc6838fa30031.bindPopup%28popup_7ff66b8f26744ec28afa454d5fc9b3c7%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e403fdf707ac4a3cb9d8df977dc127d0%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.63606285%2C%20101.063452%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_ca6208523ae747d0ab10044a60a59633%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5a4e2a92c1644e6c83f2786d34cad15c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_5a4e2a92c1644e6c83f2786d34cad15c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMee%20Tarik%20Warisan%20Asli%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_ca6208523ae747d0ab10044a60a59633.setContent%28html_5a4e2a92c1644e6c83f2786d34cad15c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_e403fdf707ac4a3cb9d8df977dc127d0.bindPopup%28popup_ca6208523ae747d0ab10044a60a59633%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_65b45c142f534fccbde7bfdda09f1dd6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.63606285%2C%20101.063452%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a1beb34e41954007a3117647a070abd2%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_85f9e3694dcc46c09708b5cfc611422c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_85f9e3694dcc46c09708b5cfc611422c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Chap%20Heng%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a1beb34e41954007a3117647a070abd2.setContent%28html_85f9e3694dcc46c09708b5cfc611422c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_65b45c142f534fccbde7bfdda09f1dd6.bindPopup%28popup_a1beb34e41954007a3117647a070abd2%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e568597895c847a9b8aaa4a5232aef33%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.63606285%2C%20101.063452%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_f17e32f60d3142d7a29ed73771db5d69%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_4e783858b7dc4348ac8304e4b7a6a11c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_4e783858b7dc4348ac8304e4b7a6a11c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EYum%20Yum%20Bak%20Kut%20Teh%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_f17e32f60d3142d7a29ed73771db5d69.setContent%28html_4e783858b7dc4348ac8304e4b7a6a11c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_e568597895c847a9b8aaa4a5232aef33.bindPopup%28popup_f17e32f60d3142d7a29ed73771db5d69%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_83b59a404bc447219dfe87acc3d1b9f9%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.63606285%2C%20101.063452%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_4641245e9dc84ec9a6800ade353802b4%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_44bef867112d475d94c5f7a3cddc0b59%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_44bef867112d475d94c5f7a3cddc0b59%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESam%20Ma%20Chicken%20Rice%20%E4%B8%89%E5%A6%88%E8%8A%BD%E8%8F%9C%E6%BB%91%E9%B8%A1%E9%A5%AD%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_4641245e9dc84ec9a6800ade353802b4.setContent%28html_44bef867112d475d94c5f7a3cddc0b59%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_83b59a404bc447219dfe87acc3d1b9f9.bindPopup%28popup_4641245e9dc84ec9a6800ade353802b4%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_18423bd3174644ec8ec1c4d1435c05d2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.63606285%2C%20101.063452%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_b1941c2b829a4052930bcd8effec047e%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1430529705fc41fa80acddc40e758c5a%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1430529705fc41fa80acddc40e758c5a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%9D%A5%E5%8F%91%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_b1941c2b829a4052930bcd8effec047e.setContent%28html_1430529705fc41fa80acddc40e758c5a%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_18423bd3174644ec8ec1c4d1435c05d2.bindPopup%28popup_b1941c2b829a4052930bcd8effec047e%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_60c7eb8855eb4f94ae6e1ebc14843ed1%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.604297842%2C%20101.058809%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_4209d23b1f974aebbbc80c4e34bd2633%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d81fa8255fe549c69196ad90dbe89548%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_d81fa8255fe549c69196ad90dbe89548%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Fu%20Lim%20%E5%AF%8C%E8%87%A8%E6%B5%B7%E9%B2%9C%E9%85%92%E5%AE%B6%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_4209d23b1f974aebbbc80c4e34bd2633.setContent%28html_d81fa8255fe549c69196ad90dbe89548%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_60c7eb8855eb4f94ae6e1ebc14843ed1.bindPopup%28popup_4209d23b1f974aebbbc80c4e34bd2633%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_010c1956edc64389b17e1599475b300f%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.604297842%2C%20101.058809%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_321633a3c30a407bb3230e4cbcd56f44%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_339730d9df174e68a5a405064b75eee5%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_339730d9df174e68a5a405064b75eee5%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%87%E8%AE%B0%E9%A5%AD%E5%BA%97%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_321633a3c30a407bb3230e4cbcd56f44.setContent%28html_339730d9df174e68a5a405064b75eee5%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_010c1956edc64389b17e1599475b300f.bindPopup%28popup_321633a3c30a407bb3230e4cbcd56f44%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_ace2ce7beac946878151b86723a324aa%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_ac436bcc7abb4242befbe8c0a503f2d1%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7f1a08fbfb33424a87b5f327ac268ad1%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_7f1a08fbfb33424a87b5f327ac268ad1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Shion%20Mun%20Lau%20%28%E5%B8%B8%E6%BB%A1%E6%A5%BC%E9%A5%AD%E5%BA%97%29%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_ac436bcc7abb4242befbe8c0a503f2d1.setContent%28html_7f1a08fbfb33424a87b5f327ac268ad1%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_ace2ce7beac946878151b86723a324aa.bindPopup%28popup_ac436bcc7abb4242befbe8c0a503f2d1%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6a75cf6a416c4228890b07158efa4126%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.586679673%2C%20101.0531579%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_d397eea9d9bd415fb40b8433bb8f7c54%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_07686c59ed064bc5b26939bebdcd94ed%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_07686c59ed064bc5b26939bebdcd94ed%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFalim%20%E9%B1%BC%E6%97%A6%E4%BB%94%E7%B2%89%E9%A5%AD%E6%A1%A3%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_d397eea9d9bd415fb40b8433bb8f7c54.setContent%28html_07686c59ed064bc5b26939bebdcd94ed%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_6a75cf6a416c4228890b07158efa4126.bindPopup%28popup_d397eea9d9bd415fb40b8433bb8f7c54%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8a676f0f3a75400bb67094d84bcc6199%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.586679673%2C%20101.0531579%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_f4bb6a4bda4c4994bb038ca1452431e8%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_75ea72ec8dd84e0bbcafd604cc58501c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_75ea72ec8dd84e0bbcafd604cc58501c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Wong%20Sheng%20%E6%97%BA%E7%9B%9B%E6%B5%B7%E9%B2%9C%E9%A5%AD%E5%BA%97%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_f4bb6a4bda4c4994bb038ca1452431e8.setContent%28html_75ea72ec8dd84e0bbcafd604cc58501c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_8a676f0f3a75400bb67094d84bcc6199.bindPopup%28popup_f4bb6a4bda4c4994bb038ca1452431e8%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_afa2d2d74e5e40c6b9a002cfabea3e2a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.58685%2C%20101.04376%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_c8195dbf19374b85b386b8d3eda32f77%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_618471499102448fa86e6236bc42991a%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_618471499102448fa86e6236bc42991a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E9%92%BB%E7%9F%B3%E5%92%96%E5%96%B1%E7%B2%89%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_c8195dbf19374b85b386b8d3eda32f77.setContent%28html_618471499102448fa86e6236bc42991a%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_afa2d2d74e5e40c6b9a002cfabea3e2a.bindPopup%28popup_c8195dbf19374b85b386b8d3eda32f77%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_50c39fab1f0a4e1fbc9cbc523bcf280c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.582193783999999%2C%20101.0846176%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_1befb7ddcadb4df59b8e7088f1327019%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7efa4f9aeae2496da25b1a82451d03d3%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_7efa4f9aeae2496da25b1a82451d03d3%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKopitiam%20Chee%20Kong%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_1befb7ddcadb4df59b8e7088f1327019.setContent%28html_7efa4f9aeae2496da25b1a82451d03d3%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_50c39fab1f0a4e1fbc9cbc523bcf280c.bindPopup%28popup_1befb7ddcadb4df59b8e7088f1327019%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_a50d26f5e3c54c6a90aa244c5ad8e4ab%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.582193783999999%2C%20101.0846176%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_e7768f087fb54c34a45fac23bc5d728a%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c20881e9bb774d83b1d2bc148d2fb552%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_c20881e9bb774d83b1d2bc148d2fb552%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%8D%97%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_e7768f087fb54c34a45fac23bc5d728a.setContent%28html_c20881e9bb774d83b1d2bc148d2fb552%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_a50d26f5e3c54c6a90aa244c5ad8e4ab.bindPopup%28popup_e7768f087fb54c34a45fac23bc5d728a%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_dfa7bf5fd6f244f19013cd0a480cc35e%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.825533055%2C%20100.7078372%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_f25c2772428e4067b1d85dd371cf4e21%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1b5dce7e01964b1392e5bee93e0dd196%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1b5dce7e01964b1392e5bee93e0dd196%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E9%BE%99%E8%AE%B0%E8%82%89%E9%AA%A8%E8%8C%B6%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_f25c2772428e4067b1d85dd371cf4e21.setContent%28html_1b5dce7e01964b1392e5bee93e0dd196%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_dfa7bf5fd6f244f19013cd0a480cc35e.bindPopup%28popup_f25c2772428e4067b1d85dd371cf4e21%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_05d2d17a54c5425f9f6db7eaf4d4501a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.825533055%2C%20100.7078372%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a2795d1558994a9c9df5498945e1a2fa%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f4da414c9dad4c71953e3119e7ebab30%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_f4da414c9dad4c71953e3119e7ebab30%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECashier%20Market%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a2795d1558994a9c9df5498945e1a2fa.setContent%28html_f4da414c9dad4c71953e3119e7ebab30%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_05d2d17a54c5425f9f6db7eaf4d4501a.bindPopup%28popup_a2795d1558994a9c9df5498945e1a2fa%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_99116cdf5d3741a29297b63f9acc79fa%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.825533055%2C%20100.7078372%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_79328772ab984e558ceca7b987dcbbf6%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_210938fa56ee47cc952409987046a7cd%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_210938fa56ee47cc952409987046a7cd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%B0%E7%BE%8E%E6%BA%90%E6%B5%B7%E9%AE%AE%E9%A3%AF%E5%BA%97%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_79328772ab984e558ceca7b987dcbbf6.setContent%28html_210938fa56ee47cc952409987046a7cd%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_99116cdf5d3741a29297b63f9acc79fa.bindPopup%28popup_79328772ab984e558ceca7b987dcbbf6%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8924fe2c5e36483a82b3b9d26c200571%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.825533055%2C%20100.7078372%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_805bf334913847f4bd6d1df7de742aa6%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f5af2976353041608e6419ac6568a54a%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_f5af2976353041608e6419ac6568a54a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EYew%20Lee%20%E6%9C%89%E5%88%A9%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_805bf334913847f4bd6d1df7de742aa6.setContent%28html_f5af2976353041608e6419ac6568a54a%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_8924fe2c5e36483a82b3b9d26c200571.bindPopup%28popup_805bf334913847f4bd6d1df7de742aa6%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c06f711ecb15468294aa4035958b37a6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.825533055%2C%20100.7078372%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_62a938070a2e436c97d49b0ae4cf9416%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_2126e48235bb42b7aeb832247f1f0dfd%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_2126e48235bb42b7aeb832247f1f0dfd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKedai%20Kopi%20Kok%20Beng%20Chicken%20Rice%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_62a938070a2e436c97d49b0ae4cf9416.setContent%28html_2126e48235bb42b7aeb832247f1f0dfd%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_c06f711ecb15468294aa4035958b37a6.bindPopup%28popup_62a938070a2e436c97d49b0ae4cf9416%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_4489c5540a8248fe8c6483285e184f3f%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.825533055%2C%20100.7078372%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_e4b301cb0e684451b73b6a5cf623fba1%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_99a6268a31da4eaea6514e569d8f3b11%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_99a6268a31da4eaea6514e569d8f3b11%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E7%A6%8F%E6%BB%A1%E6%A5%BC%E6%B5%B7%E9%B2%9C%E7%B2%A5%2C%2030100%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_e4b301cb0e684451b73b6a5cf623fba1.setContent%28html_99a6268a31da4eaea6514e569d8f3b11%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_4489c5540a8248fe8c6483285e184f3f.bindPopup%28popup_e4b301cb0e684451b73b6a5cf623fba1%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_f6b9e65895ac45688966998297643fc1%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.6055199999999985%2C%20101.09879%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_488b2be5f06b4244bd8fbe47684ff62a%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_fca2338d1b5d4cdbbb6416c4097c1416%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_fca2338d1b5d4cdbbb6416c4097c1416%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESam%20Ma%20Chicken%20Rice%20%E4%B8%89%E5%A6%88%E8%8A%BD%E8%8F%9C%E6%BB%91%E9%B8%A1%E9%A5%AD%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_488b2be5f06b4244bd8fbe47684ff62a.setContent%28html_fca2338d1b5d4cdbbb6416c4097c1416%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_f6b9e65895ac45688966998297643fc1.bindPopup%28popup_488b2be5f06b4244bd8fbe47684ff62a%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c5c44105fa41403c9dc1772b7a83f866%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.6055199999999985%2C%20101.09879%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_cf037c5f2fef40b9be5c44a1a6d818b5%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7e2db859c7e648029648884a297f79c1%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_7e2db859c7e648029648884a297f79c1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EYum%20Yum%20Bak%20Kut%20Teh%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_cf037c5f2fef40b9be5c44a1a6d818b5.setContent%28html_7e2db859c7e648029648884a297f79c1%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_c5c44105fa41403c9dc1772b7a83f866.bindPopup%28popup_cf037c5f2fef40b9be5c44a1a6d818b5%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5d0de051cdbe4345a94368d82256f4b5%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.6055199999999985%2C%20101.09879%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_b7f17feeb8f74c418ad4c41eec66c1f7%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_b20ce5ca163945e08ea253450bf2a557%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_b20ce5ca163945e08ea253450bf2a557%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Fu%20Lim%20%E5%AF%8C%E8%87%A8%E6%B5%B7%E9%B2%9C%E9%85%92%E5%AE%B6%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_b7f17feeb8f74c418ad4c41eec66c1f7.setContent%28html_b20ce5ca163945e08ea253450bf2a557%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_5d0de051cdbe4345a94368d82256f4b5.bindPopup%28popup_b7f17feeb8f74c418ad4c41eec66c1f7%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9a7e033bfb3a4457ae80b078b8dc69f0%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.60053%2C%20101.09515%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_16968cb4dfc344dea9ff41ef8a210091%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e809cb14b6cc4e6999d23283ba65a6e2%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_e809cb14b6cc4e6999d23283ba65a6e2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%9D%A5%E5%8F%91%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_16968cb4dfc344dea9ff41ef8a210091.setContent%28html_e809cb14b6cc4e6999d23283ba65a6e2%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_9a7e033bfb3a4457ae80b078b8dc69f0.bindPopup%28popup_16968cb4dfc344dea9ff41ef8a210091%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e5c97b8b57ba41fcac17a5232ef6b13a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.60053%2C%20101.09515%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_59fb44474ccd40a78b61e5ceedaeae4d%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_754ab79e04fd4450930a5ee51f0b8133%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_754ab79e04fd4450930a5ee51f0b8133%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Chap%20Heng%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_59fb44474ccd40a78b61e5ceedaeae4d.setContent%28html_754ab79e04fd4450930a5ee51f0b8133%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_e5c97b8b57ba41fcac17a5232ef6b13a.bindPopup%28popup_59fb44474ccd40a78b61e5ceedaeae4d%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_59026b377b66489c86f9bcb397324ceb%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.589598167%2C%20101.0786996%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_2cbddc0fd5484849a28685e2b1845e8e%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_eea5f2efc41540838f47de18cc2fde87%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_eea5f2efc41540838f47de18cc2fde87%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%87%E8%AE%B0%E9%A5%AD%E5%BA%97%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_2cbddc0fd5484849a28685e2b1845e8e.setContent%28html_eea5f2efc41540838f47de18cc2fde87%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_59026b377b66489c86f9bcb397324ceb.bindPopup%28popup_2cbddc0fd5484849a28685e2b1845e8e%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6ab4da76346b4fc4bb519794777c6424%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.604167909%2C%20101.0886988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_585804936db24d6d8327cbe7808aa43d%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_de8c15548a194ec099a7a2a1bd1a0826%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_de8c15548a194ec099a7a2a1bd1a0826%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFamous%20Jelapang%20Road%20Side%20Laksa%20And%20Fruit%20Rojak%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_585804936db24d6d8327cbe7808aa43d.setContent%28html_de8c15548a194ec099a7a2a1bd1a0826%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_6ab4da76346b4fc4bb519794777c6424.bindPopup%28popup_585804936db24d6d8327cbe7808aa43d%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_2c8da3ad13a448d6b7a47a4f5b140151%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.609967775%2C%20101.0767172%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_5cdba91780e947fb948f32a0a862eded%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_48006f2680fb423a9afe340fca105d42%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_48006f2680fb423a9afe340fca105d42%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMee%20Tarik%20Warisan%20Asli%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_5cdba91780e947fb948f32a0a862eded.setContent%28html_48006f2680fb423a9afe340fca105d42%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_2c8da3ad13a448d6b7a47a4f5b140151.bindPopup%28popup_5cdba91780e947fb948f32a0a862eded%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_2cc2213a46684356a73079b0f9c90181%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.5801356580000006%2C%20101.0986729%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_d7420c0f89554c9e97011a81adbf9800%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_edd85ed1a34647c4af875e92df1de4ad%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_edd85ed1a34647c4af875e92df1de4ad%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Shion%20Mun%20Lau%20%28%E5%B8%B8%E6%BB%A1%E6%A5%BC%E9%A5%AD%E5%BA%97%29%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_d7420c0f89554c9e97011a81adbf9800.setContent%28html_edd85ed1a34647c4af875e92df1de4ad%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_2cc2213a46684356a73079b0f9c90181.bindPopup%28popup_d7420c0f89554c9e97011a81adbf9800%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b373387cc9a248a18a8444a22d54bf49%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.212019818%2C%20101.2532391%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a0ae5543a8b744d9a37077ecb633378b%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1662aa15752b4ca1afed05b4547d93ee%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1662aa15752b4ca1afed05b4547d93ee%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E9%A3%9F%E4%B9%8B%E5%91%B3%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a0ae5543a8b744d9a37077ecb633378b.setContent%28html_1662aa15752b4ca1afed05b4547d93ee%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_b373387cc9a248a18a8444a22d54bf49.bindPopup%28popup_a0ae5543a8b744d9a37077ecb633378b%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_49bbb0f8a0654856a8ce3beebebc34d5%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.212019818%2C%20101.2532391%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_90e5322f3155406da7c0d22ac3507e7a%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_fbc0a89953e74fdc91ccf65f2aa1195d%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_fbc0a89953e74fdc91ccf65f2aa1195d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESizzling%20Wok%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_90e5322f3155406da7c0d22ac3507e7a.setContent%28html_fbc0a89953e74fdc91ccf65f2aa1195d%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_49bbb0f8a0654856a8ce3beebebc34d5.bindPopup%28popup_90e5322f3155406da7c0d22ac3507e7a%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5950317c5a8a4d2ebb2f4bc0c81a1598%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.212019818%2C%20101.2532391%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_17c3a3ef453a4a3ca3904558d8e3d6d6%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6354f7efa83945d5aed3c5affab67979%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_6354f7efa83945d5aed3c5affab67979%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHou%20Yi%20Lou%20Restaurant%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_17c3a3ef453a4a3ca3904558d8e3d6d6.setContent%28html_6354f7efa83945d5aed3c5affab67979%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_5950317c5a8a4d2ebb2f4bc0c81a1598.bindPopup%28popup_17c3a3ef453a4a3ca3904558d8e3d6d6%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1e331d28aaee4f1cb4c5f350c4ca3315%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.212019818%2C%20101.2532391%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a3f0d9350c9e4ec6afd4608f77ab3293%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7b449f866c2c428d896d0353c6cbbf1c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_7b449f866c2c428d896d0353c6cbbf1c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%8D%97%E8%88%88%E9%9A%86%E6%B5%B7%E9%AE%AE%E9%A3%AF%E5%BA%97%20Nam%20Hing%20Loong%20Restaurant%2C%2030450%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a3f0d9350c9e4ec6afd4608f77ab3293.setContent%28html_7b449f866c2c428d896d0353c6cbbf1c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1e331d28aaee4f1cb4c5f350c4ca3315.bindPopup%28popup_a3f0d9350c9e4ec6afd4608f77ab3293%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_43722600487c4e259909855e77fd3328%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.8%2C%20100.9%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_40799c85e9b74e89ad342bf375840102%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_4a8ae396747e41edab436256b69464be%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_4a8ae396747e41edab436256b69464be%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%B1%9F%E6%B2%99%E7%89%9B%E8%82%89%E9%9D%A2%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_40799c85e9b74e89ad342bf375840102.setContent%28html_4a8ae396747e41edab436256b69464be%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_43722600487c4e259909855e77fd3328.bindPopup%28popup_40799c85e9b74e89ad342bf375840102%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_ce3202b31df648d78330afb0c607a039%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.8%2C%20100.9%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_682cb5f033ca4bff9706e2a51e552ed8%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_23eb3749ce484aee96d7b7661bfee1ee%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_23eb3749ce484aee96d7b7661bfee1ee%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%88%A9%E6%B0%91%E5%8A%A0%E5%9C%B0%E5%B0%8F%E9%A3%9F%E4%B8%AD%E5%BF%83%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_682cb5f033ca4bff9706e2a51e552ed8.setContent%28html_23eb3749ce484aee96d7b7661bfee1ee%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_ce3202b31df648d78330afb0c607a039.bindPopup%28popup_682cb5f033ca4bff9706e2a51e552ed8%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6e3008fa7746446f99b29ea06f2d055b%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.41522%2C%20100.96175%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_acb5727011a94dfea1a05e18bb6c075f%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6894539c578744bfa0528a25dd16174b%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_6894539c578744bfa0528a25dd16174b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKheng%20Hiong%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_acb5727011a94dfea1a05e18bb6c075f.setContent%28html_6894539c578744bfa0528a25dd16174b%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_6e3008fa7746446f99b29ea06f2d055b.bindPopup%28popup_acb5727011a94dfea1a05e18bb6c075f%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_145e38578b9c4bfc91bdb05b985526d5%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.41522%2C%20100.96175%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_7f8cab8f62c742c8ab30b40ead408afb%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_94b1ac16dfb240d1ad1d272a427abce7%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_94b1ac16dfb240d1ad1d272a427abce7%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Yin%20Fei%20%E6%99%8F%E8%8F%B2%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_7f8cab8f62c742c8ab30b40ead408afb.setContent%28html_94b1ac16dfb240d1ad1d272a427abce7%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_145e38578b9c4bfc91bdb05b985526d5.bindPopup%28popup_7f8cab8f62c742c8ab30b40ead408afb%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9579f3ec95e74b78902a25b8144d49a2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.41522%2C%20100.96175%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_3d7223cb858a4be1b5780244dca0eea2%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1a1db863f8b94745aa4b961097d161de%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1a1db863f8b94745aa4b961097d161de%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Choy%20Pin%20%28%E8%90%8D%E8%90%8D%E8%8C%B6%E9%A4%90%E5%AE%A4%29%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_3d7223cb858a4be1b5780244dca0eea2.setContent%28html_1a1db863f8b94745aa4b961097d161de%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_9579f3ec95e74b78902a25b8144d49a2.bindPopup%28popup_3d7223cb858a4be1b5780244dca0eea2%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_7f7c950eb13147c0a68fc0a3bb335989%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_2bbad5f34bda45a0a1281f0a8e51d32d%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c90f9597ce6847af8ea4d493ba698dd0%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_c90f9597ce6847af8ea4d493ba698dd0%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESam%20Ma%20Chicken%20Rice%20%E4%B8%89%E5%A6%88%E8%8A%BD%E8%8F%9C%E6%BB%91%E9%B8%A1%E9%A5%AD%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_2bbad5f34bda45a0a1281f0a8e51d32d.setContent%28html_c90f9597ce6847af8ea4d493ba698dd0%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_7f7c950eb13147c0a68fc0a3bb335989.bindPopup%28popup_2bbad5f34bda45a0a1281f0a8e51d32d%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_3d21e44bb0d34263bbb109f1cb97f94a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_ae99a66ea5a041ddb87f930673839107%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e54d7141da5b4747b435f362dd10434b%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_e54d7141da5b4747b435f362dd10434b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EYum%20Yum%20Bak%20Kut%20Teh%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_ae99a66ea5a041ddb87f930673839107.setContent%28html_e54d7141da5b4747b435f362dd10434b%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_3d21e44bb0d34263bbb109f1cb97f94a.bindPopup%28popup_ae99a66ea5a041ddb87f930673839107%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_70a093895f7345de8a352cc2f51e1740%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.59857%2C%20101.11988%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_98e8159712744fa5aaa164c849561664%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_b6789fc732414c9d8c5778afc2d3f18c%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_b6789fc732414c9d8c5778afc2d3f18c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Shion%20Mun%20Lau%20%28%E5%B8%B8%E6%BB%A1%E6%A5%BC%E9%A5%AD%E5%BA%97%29%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_98e8159712744fa5aaa164c849561664.setContent%28html_b6789fc732414c9d8c5778afc2d3f18c%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_70a093895f7345de8a352cc2f51e1740.bindPopup%28popup_98e8159712744fa5aaa164c849561664%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_ea43bb7537a84e47864c78f53afa7596%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B5.16111%2C%20100.68044%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_fe655b88cfb94032b88e972967c1074b%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_b480e9a8d1ca4b348ef31d2baff46346%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_b480e9a8d1ca4b348ef31d2baff46346%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESerdang%E6%98%93%E8%AE%B0%E6%B5%B7%E9%B2%9C%E6%A1%A3%28%E7%82%92%E7%B2%A5%29%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_fe655b88cfb94032b88e972967c1074b.setContent%28html_b480e9a8d1ca4b348ef31d2baff46346%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_ea43bb7537a84e47864c78f53afa7596.bindPopup%28popup_fe655b88cfb94032b88e972967c1074b%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1e54858a495b4fb2b44a994ac1b0aa75%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B5.16111%2C%20100.68044%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_58fe71ee1daf4889837e43186520fa99%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c2964299f527437dab5422a75e33cd97%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_c2964299f527437dab5422a75e33cd97%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Bie%20You%20Tian%20%E5%88%AB%E6%9C%89%E5%A4%A9%E6%B5%B7%E9%B2%9C%20%28%E5%92%96%E5%93%A9%E5%B1%B1%E7%8C%AA%E8%82%89%29%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_58fe71ee1daf4889837e43186520fa99.setContent%28html_c2964299f527437dab5422a75e33cd97%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_1e54858a495b4fb2b44a994ac1b0aa75.bindPopup%28popup_58fe71ee1daf4889837e43186520fa99%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_160a6ef0b2d14ed8b30edd9d72e5b909%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B5.16111%2C%20100.68044%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_448d9f4a29854f7fa39224e68a5a2ef2%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_4b5e6af71e2d48a9941b928f8d4471ab%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_4b5e6af71e2d48a9941b928f8d4471ab%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESin%20Aik%20Kee%20Restaurant%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_448d9f4a29854f7fa39224e68a5a2ef2.setContent%28html_4b5e6af71e2d48a9941b928f8d4471ab%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_160a6ef0b2d14ed8b30edd9d72e5b909.bindPopup%28popup_448d9f4a29854f7fa39224e68a5a2ef2%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_32e4c057faed46cb9217c2874956bc01%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.541906668%2C%20101.0729075%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_436c3d45835642a8bcca739aa3676415%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_a759fcba95604387900ca7eba4cf7425%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_a759fcba95604387900ca7eba4cf7425%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%9D%A5%E5%8F%91%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_436c3d45835642a8bcca739aa3676415.setContent%28html_a759fcba95604387900ca7eba4cf7425%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_32e4c057faed46cb9217c2874956bc01.bindPopup%28popup_436c3d45835642a8bcca739aa3676415%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_0c6f1858cb784374b37f3d2d37d6f219%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.541906668%2C%20101.0729075%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_d786a331324d4868b5693bb9af215965%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7ee9dc90414149dfa8b8c65d2d2d6546%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_7ee9dc90414149dfa8b8c65d2d2d6546%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Fu%20Lim%20%E5%AF%8C%E8%87%A8%E6%B5%B7%E9%B2%9C%E9%85%92%E5%AE%B6%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_d786a331324d4868b5693bb9af215965.setContent%28html_7ee9dc90414149dfa8b8c65d2d2d6546%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_0c6f1858cb784374b37f3d2d37d6f219.bindPopup%28popup_d786a331324d4868b5693bb9af215965%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_3b9c7b93f85a4ad4a0314528189b1f25%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.541906668%2C%20101.0729075%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_6cf37771a3054f1fa4eaa85d358e6b13%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_a689ea53cc4a43638d79f1aa3d4ff1fe%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_a689ea53cc4a43638d79f1aa3d4ff1fe%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%87%E8%AE%B0%E9%A5%AD%E5%BA%97%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_6cf37771a3054f1fa4eaa85d358e6b13.setContent%28html_a689ea53cc4a43638d79f1aa3d4ff1fe%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_3b9c7b93f85a4ad4a0314528189b1f25.bindPopup%28popup_6cf37771a3054f1fa4eaa85d358e6b13%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_98a94b83b3d447678312e211bf547583%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.541906668%2C%20101.0729075%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_dfdb59edeb1e4ab0843c97f3e9e130b4%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_cb429689d41445d1a042e3cdcd665ce2%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_cb429689d41445d1a042e3cdcd665ce2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKedai%20Kopi%20You%20Like%20It%20%E5%A5%BD%E9%94%BA%E6%84%8F%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_dfdb59edeb1e4ab0843c97f3e9e130b4.setContent%28html_cb429689d41445d1a042e3cdcd665ce2%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_98a94b83b3d447678312e211bf547583.bindPopup%28popup_dfdb59edeb1e4ab0843c97f3e9e130b4%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_750577573994495695c1fc5563f52bfa%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.525305035%2C%20101.0287701%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_6de6bfaeec3a40d894223e470ff3155c%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_2efd1a1a4d57437cb7391355a0cc44d9%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_2efd1a1a4d57437cb7391355a0cc44d9%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Ming%20Feong%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_6de6bfaeec3a40d894223e470ff3155c.setContent%28html_2efd1a1a4d57437cb7391355a0cc44d9%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_750577573994495695c1fc5563f52bfa.bindPopup%28popup_6de6bfaeec3a40d894223e470ff3155c%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6fe40b5dea6e445ab8a905bef148c60c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.525305035%2C%20101.0287701%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_59f8bac9605a4299b15d42f8433b7790%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_a94fe101f7194e849519aff54a327104%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_a94fe101f7194e849519aff54a327104%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E9%92%BB%E7%9F%B3%E5%92%96%E5%96%B1%E7%B2%89%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_59f8bac9605a4299b15d42f8433b7790.setContent%28html_a94fe101f7194e849519aff54a327104%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_6fe40b5dea6e445ab8a905bef148c60c.bindPopup%28popup_59f8bac9605a4299b15d42f8433b7790%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_37064271e96744a59a2d30531a9b6467%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.525305035%2C%20101.0287701%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_9659eb181b844ca0863bd4a2c843d324%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1d5a03b93f6b4ac48b51f659bd99557a%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1d5a03b93f6b4ac48b51f659bd99557a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Chap%20Heng%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_9659eb181b844ca0863bd4a2c843d324.setContent%28html_1d5a03b93f6b4ac48b51f659bd99557a%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_37064271e96744a59a2d30531a9b6467.bindPopup%28popup_9659eb181b844ca0863bd4a2c843d324%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d2b3139c0486438b82f121db7fafa530%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.525305035%2C%20101.0287701%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_b4d433eeb649424d8f4cfcef12c39f1d%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_0a3dbf91f84245c1ad15df2bb1068b60%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_0a3dbf91f84245c1ad15df2bb1068b60%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFalim%20%E9%B1%BC%E6%97%A6%E4%BB%94%E7%B2%89%E9%A5%AD%E6%A1%A3%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_b4d433eeb649424d8f4cfcef12c39f1d.setContent%28html_0a3dbf91f84245c1ad15df2bb1068b60%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_d2b3139c0486438b82f121db7fafa530.bindPopup%28popup_b4d433eeb649424d8f4cfcef12c39f1d%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_221b914a39bf4aeb9c43264de69fd6f6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.525305035%2C%20101.0287701%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_6768885ccbf74f9b86566bfe2c1a0b61%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c343eff9b21c4da891bf2b9d5e77a1a7%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_c343eff9b21c4da891bf2b9d5e77a1a7%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERainbow%20Seafood%20Restaurant%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_6768885ccbf74f9b86566bfe2c1a0b61.setContent%28html_c343eff9b21c4da891bf2b9d5e77a1a7%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_221b914a39bf4aeb9c43264de69fd6f6.bindPopup%28popup_6768885ccbf74f9b86566bfe2c1a0b61%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_01b0d7f4dffd4c47a9c401845403e1ba%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.525305035%2C%20101.0287701%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_257d1768c0984f01809db886f13c801a%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_77b835e426af4503bc533402ada6fad0%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_77b835e426af4503bc533402ada6fad0%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%A4%A9%E8%99%B9%E6%B5%B7%E9%B2%9C%E9%85%92%E5%AE%B6%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_257d1768c0984f01809db886f13c801a.setContent%28html_77b835e426af4503bc533402ada6fad0%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_01b0d7f4dffd4c47a9c401845403e1ba.bindPopup%28popup_257d1768c0984f01809db886f13c801a%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_f322fdd860fa4d2e8d77ac2a871d170a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.525305035%2C%20101.0287701%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_88c71532b1234392a5e4dfe7a1e2c911%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_3244816511944190b461a5f1c2e03e66%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_3244816511944190b461a5f1c2e03e66%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Wong%20Sheng%20%E6%97%BA%E7%9B%9B%E6%B5%B7%E9%B2%9C%E9%A5%AD%E5%BA%97%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_88c71532b1234392a5e4dfe7a1e2c911.setContent%28html_3244816511944190b461a5f1c2e03e66%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_f322fdd860fa4d2e8d77ac2a871d170a.bindPopup%28popup_88c71532b1234392a5e4dfe7a1e2c911%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_ad04da5d5e6e43e29da04dd22ab49325%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.63972%2C%20101.1304%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a2aca1b0ee23464d847467d14cedbbf3%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e8e6187f9287404b913d1628558a646f%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_e8e6187f9287404b913d1628558a646f%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKopitiam%20Chee%20Kong%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a2aca1b0ee23464d847467d14cedbbf3.setContent%28html_e8e6187f9287404b913d1628558a646f%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_ad04da5d5e6e43e29da04dd22ab49325.bindPopup%28popup_a2aca1b0ee23464d847467d14cedbbf3%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_f6e1c2f6a3c74e2d838c630167d82e20%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.63972%2C%20101.1304%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_1fc2a0cd8f9c43239b9918bc3303b889%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_657af2e67fe4495bb75a9fe00b9e73f2%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_657af2e67fe4495bb75a9fe00b9e73f2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMee%20Tarik%20Warisan%20Asli%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_1fc2a0cd8f9c43239b9918bc3303b889.setContent%28html_657af2e67fe4495bb75a9fe00b9e73f2%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_f6e1c2f6a3c74e2d838c630167d82e20.bindPopup%28popup_1fc2a0cd8f9c43239b9918bc3303b889%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d4e27e19e51347a3836b2faed5594829%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.621691575%2C%20101.0562687%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_f864cbf32aab4e418f43356d1032cb80%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_638e6422cc19472298e08e916e599527%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_638e6422cc19472298e08e916e599527%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFamous%20Jelapang%20Road%20Side%20Laksa%20And%20Fruit%20Rojak%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_f864cbf32aab4e418f43356d1032cb80.setContent%28html_638e6422cc19472298e08e916e599527%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_d4e27e19e51347a3836b2faed5594829.bindPopup%28popup_f864cbf32aab4e418f43356d1032cb80%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_00e97d1cf4404903b1a23a5e6020eadd%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.576582902%2C%20101.0769685%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_3dc5e600131f42dab0b2cb9fc4bd5a07%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e12d9d69d33445d2bcd574bf88bf7ce9%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_e12d9d69d33445d2bcd574bf88bf7ce9%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%8D%97%E8%8C%B6%E9%A4%90%E5%AE%A4%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_3dc5e600131f42dab0b2cb9fc4bd5a07.setContent%28html_e12d9d69d33445d2bcd574bf88bf7ce9%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_00e97d1cf4404903b1a23a5e6020eadd.bindPopup%28popup_3dc5e600131f42dab0b2cb9fc4bd5a07%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6c60ba3cdbc34454943156718baa432f%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.56848%2C%20101.07701%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_29481adaf73241c2a071f18f4a77bfc9%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_4b188c274726425bac9a63a8427e4ab7%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_4b188c274726425bac9a63a8427e4ab7%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHong%20Kong%20Oil%20Chicken%20%26amp%3B%20Roast%20Duck%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_29481adaf73241c2a071f18f4a77bfc9.setContent%28html_4b188c274726425bac9a63a8427e4ab7%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_6c60ba3cdbc34454943156718baa432f.bindPopup%28popup_29481adaf73241c2a071f18f4a77bfc9%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_ee0a9769fcc64257b97b50580f7086de%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.544485564%2C%20101.0670942%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_927f317d764a4009afcf26fe990870cf%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_41e44ea9c2e24c44940897ea611c34a5%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_41e44ea9c2e24c44940897ea611c34a5%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Mee%20Fong%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_927f317d764a4009afcf26fe990870cf.setContent%28html_41e44ea9c2e24c44940897ea611c34a5%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_ee0a9769fcc64257b97b50580f7086de.bindPopup%28popup_927f317d764a4009afcf26fe990870cf%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_628d52a302c141459a0a679cf1ddffd8%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.575243143%2C%20101.0707209%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_6132185da7c2427fa0f965e6f7ee170a%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1df46291be014c7bbecc36e28dba27d2%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1df46291be014c7bbecc36e28dba27d2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKFG%20Claypot%20Chicken%20Rice%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_6132185da7c2427fa0f965e6f7ee170a.setContent%28html_1df46291be014c7bbecc36e28dba27d2%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_628d52a302c141459a0a679cf1ddffd8.bindPopup%28popup_6132185da7c2427fa0f965e6f7ee170a%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_99754b6c885a41348281f7aee7031d3b%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.2461400000000005%2C%20100.75734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_3392ebc9180a4a04a9cb28d44c21ce13%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d22b477f7a4c4b2dbf6b19b3693e52da%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_d22b477f7a4c4b2dbf6b19b3693e52da%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestaurant%20Michelin%20Star%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_3392ebc9180a4a04a9cb28d44c21ce13.setContent%28html_d22b477f7a4c4b2dbf6b19b3693e52da%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_99754b6c885a41348281f7aee7031d3b.bindPopup%28popup_3392ebc9180a4a04a9cb28d44c21ce13%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_60d110c520ed44e59cd30ca681253d4a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.2461400000000005%2C%20100.75734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_90b203b8dffc434a9e891ba54bc1b374%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1e341884a8dc4aafb1cd8d14abafaabd%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_1e341884a8dc4aafb1cd8d14abafaabd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E7%BE%A4%E8%8F%AF%E6%B5%B7%E9%AE%AE%E5%9C%93%E9%85%92%E5%AE%B6%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_90b203b8dffc434a9e891ba54bc1b374.setContent%28html_1e341884a8dc4aafb1cd8d14abafaabd%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_60d110c520ed44e59cd30ca681253d4a.bindPopup%28popup_90b203b8dffc434a9e891ba54bc1b374%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5f9ec47e20dd4541817fea43425840b6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.2461400000000005%2C%20100.75734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a176ebfdd808428b938bc1053f6c1bc0%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7201fe811769418589456573fe7f2716%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_7201fe811769418589456573fe7f2716%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%B0%E4%B8%80%E8%89%B2%E8%8C%B6%E9%A4%90%E5%AE%A4%20Restoran%20Sin%20Ek%20Sek%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a176ebfdd808428b938bc1053f6c1bc0.setContent%28html_7201fe811769418589456573fe7f2716%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_5f9ec47e20dd4541817fea43425840b6.bindPopup%28popup_a176ebfdd808428b938bc1053f6c1bc0%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_07f9c24a04754aff91a5fc2cdef2b6ab%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.2461400000000005%2C%20100.75734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_aba64272215947b19942beed068d8d8b%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_a13a998ce4c6476fb9eb18d59217d1c3%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_a13a998ce4c6476fb9eb18d59217d1c3%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EKampung%20Koh%20Corner%20Mee%20Stall%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_aba64272215947b19942beed068d8d8b.setContent%28html_a13a998ce4c6476fb9eb18d59217d1c3%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_07f9c24a04754aff91a5fc2cdef2b6ab.bindPopup%28popup_aba64272215947b19942beed068d8d8b%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_0b649caf736f480fb8c6fc484fa3c1ca%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.2461400000000005%2C%20100.75734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_a51e39e576e246418e44e7a929b1da26%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_8b2ee6326f8044c7952f27023e6041fe%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_8b2ee6326f8044c7952f27023e6041fe%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EAmu%20Coconut%20Villa%20Restaurant%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_a51e39e576e246418e44e7a929b1da26.setContent%28html_8b2ee6326f8044c7952f27023e6041fe%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_0b649caf736f480fb8c6fc484fa3c1ca.bindPopup%28popup_a51e39e576e246418e44e7a929b1da26%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e5cbb978ec7d4dd69c141a43f74b5c20%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.2461400000000005%2C%20100.75734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_60e2d1ce97eb41ba9a78522dda531229%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_9febcf39e1504d85a86a94c3586a748e%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_9febcf39e1504d85a86a94c3586a748e%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E6%96%B0%E6%B1%89%E5%95%86%E9%85%92%E6%A5%BC%20Restoran%20Sun%20Hon%20Siong%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_60e2d1ce97eb41ba9a78522dda531229.setContent%28html_9febcf39e1504d85a86a94c3586a748e%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_e5cbb978ec7d4dd69c141a43f74b5c20.bindPopup%28popup_60e2d1ce97eb41ba9a78522dda531229%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_cedfac8feff043bbb76a5be7e9da2753%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.2461400000000005%2C%20100.75734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_b24d9838f96e4d07b5e6e9da00768a3e%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bc17e88933b54c43a1dcc6c54b75fe8a%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_bc17e88933b54c43a1dcc6c54b75fe8a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERestoran%20Ah%20Hing%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_b24d9838f96e4d07b5e6e9da00768a3e.setContent%28html_bc17e88933b54c43a1dcc6c54b75fe8a%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_cedfac8feff043bbb76a5be7e9da2753.bindPopup%28popup_b24d9838f96e4d07b5e6e9da00768a3e%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d03ac7a9d9074bd7a4e80470201f5789%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B4.2461400000000005%2C%20100.75734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%22bubblingMouseEvents%22%3A%20true%2C%20%22color%22%3A%20%22red%22%2C%20%22dashArray%22%3A%20null%2C%20%22dashOffset%22%3A%20null%2C%20%22fill%22%3A%20true%2C%20%22fillColor%22%3A%20%22%2387cefa%22%2C%20%22fillOpacity%22%3A%200.5%2C%20%22fillRule%22%3A%20%22evenodd%22%2C%20%22lineCap%22%3A%20%22round%22%2C%20%22lineJoin%22%3A%20%22round%22%2C%20%22opacity%22%3A%201.0%2C%20%22radius%22%3A%204%2C%20%22stroke%22%3A%20true%2C%20%22weight%22%3A%203%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_8c0992bb3c7e4768ba5f5de58d473bb9%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20var%20popup_8bac55527e134e30abd24693b11fe218%20%3D%20L.popup%28%7B%22maxWidth%22%3A%20%22100%25%22%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20html_30016af58f00439d9e77046cdeb9a3e7%20%3D%20%24%28%60%3Cdiv%20id%3D%22html_30016af58f00439d9e77046cdeb9a3e7%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3E%E5%AF%8C%E5%BC%BA%E6%9D%BF%E9%9D%A2%2C%2031350%3C/div%3E%60%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20popup_8bac55527e134e30abd24693b11fe218.setContent%28html_30016af58f00439d9e77046cdeb9a3e7%29%3B%0A%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20circle_marker_d03ac7a9d9074bd7a4e80470201f5789.bindPopup%28popup_8bac55527e134e30abd24693b11fe218%29%0A%20%20%20%20%20%20%20%20%3B%0A%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%3C/script%3E onload=\"this.contentDocument.open();this.contentDocument.write(    decodeURIComponent(this.getAttribute('data-html')));this.contentDocument.close();\" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>"
      ],
      "text/plain": [
       "<folium.folium.Map at 0x13b7a2a7988>"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "map_top5 = folium.Map(location=[latitude, longitude], zoom_start=12)\n",
    "for lat, lng, name, postalcode in zip(top5_df['Latitude'], top5_df['Longitude'], top5_df['Name'], top5_df['Postcode']):\n",
    "    label = '{}, {}'.format(name, postalcode)\n",
    "    label = folium.Popup(label, parse_html=True)\n",
    "    folium.CircleMarker(\n",
    "        [lat, lng],\n",
    "        radius=4,\n",
    "        popup=label,\n",
    "        color='red',\n",
    "        fill=True,\n",
    "        fill_color='#87cefa',\n",
    "        fill_opacity=0.5,\n",
    "        parse_html=False).add_to(map_top5)\n",
    "map_top5"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "From the map we can hover over the data points and view the name of the restaurant in the location"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**LETS SEE WHAT RESTURANTS ARE IN 31350**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "top5_df.drop(['ID','Unnamed: 0'],axis=1, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Location</th>\n",
       "      <th>Postcode</th>\n",
       "      <th>Name</th>\n",
       "      <th>Latitude</th>\n",
       "      <th>Longitude</th>\n",
       "      <th>Category</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>4103</th>\n",
       "      <td>RPT Jaya Tambahan 2</td>\n",
       "      <td>31350</td>\n",
       "      <td>江沙牛肉面</td>\n",
       "      <td>4.800000</td>\n",
       "      <td>100.900000</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4104</th>\n",
       "      <td>RPT Jaya Tambahan 2</td>\n",
       "      <td>31350</td>\n",
       "      <td>利民加地小食中心</td>\n",
       "      <td>4.800000</td>\n",
       "      <td>100.900000</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4105</th>\n",
       "      <td>Jalan Palma (B/6 - B/15)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Kheng Hiong</td>\n",
       "      <td>4.415220</td>\n",
       "      <td>100.961750</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4106</th>\n",
       "      <td>Jalan Palma (B/6 - B/15)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restoran Yin Fei 晏菲茶餐室</td>\n",
       "      <td>4.415220</td>\n",
       "      <td>100.961750</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4107</th>\n",
       "      <td>Jalan Palma (B/6 - B/15)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restaurant Choy Pin (萍萍茶餐室)</td>\n",
       "      <td>4.415220</td>\n",
       "      <td>100.961750</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4108</th>\n",
       "      <td>Jalan Rapat Ria (1 - 4)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Sam Ma Chicken Rice 三妈芽菜滑鸡饭</td>\n",
       "      <td>4.598570</td>\n",
       "      <td>101.119880</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4109</th>\n",
       "      <td>Jalan Rapat Ria (1 - 4)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Yum Yum Bak Kut Teh</td>\n",
       "      <td>4.598570</td>\n",
       "      <td>101.119880</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4110</th>\n",
       "      <td>Jalan Rapat Ria (1 - 4)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restaurant Shion Mun Lau (常满楼饭店)</td>\n",
       "      <td>4.598570</td>\n",
       "      <td>101.119880</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4111</th>\n",
       "      <td>Jalan Tasik Botani (A/1 - A/7)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Serdang易记海鲜档(炒粥)</td>\n",
       "      <td>5.161110</td>\n",
       "      <td>100.680440</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4112</th>\n",
       "      <td>Jalan Tasik Botani (A/1 - A/7)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restoran Bie You Tian 别有天海鲜 (咖哩山猪肉)</td>\n",
       "      <td>5.161110</td>\n",
       "      <td>100.680440</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4113</th>\n",
       "      <td>Jalan Tasik Botani (A/1 - A/7)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Sin Aik Kee Restaurant</td>\n",
       "      <td>5.161110</td>\n",
       "      <td>100.680440</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4115</th>\n",
       "      <td>Pengakalan Tiara</td>\n",
       "      <td>31350</td>\n",
       "      <td>来发茶餐室</td>\n",
       "      <td>4.541907</td>\n",
       "      <td>101.072907</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4116</th>\n",
       "      <td>Pengakalan Tiara</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restoran Fu Lim 富臨海鲜酒家</td>\n",
       "      <td>4.541907</td>\n",
       "      <td>101.072907</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4118</th>\n",
       "      <td>Pengakalan Tiara</td>\n",
       "      <td>31350</td>\n",
       "      <td>文记饭店</td>\n",
       "      <td>4.541907</td>\n",
       "      <td>101.072907</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4119</th>\n",
       "      <td>Pengakalan Tiara</td>\n",
       "      <td>31350</td>\n",
       "      <td>Kedai Kopi You Like It 好锺意茶餐室</td>\n",
       "      <td>4.541907</td>\n",
       "      <td>101.072907</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4120</th>\n",
       "      <td>Persiaran Tasik Botani (1 - 2)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restoran Ming Feong</td>\n",
       "      <td>4.525305</td>\n",
       "      <td>101.028770</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4125</th>\n",
       "      <td>Persiaran Tasik Botani (1 - 2)</td>\n",
       "      <td>31350</td>\n",
       "      <td>钻石咖喱粉</td>\n",
       "      <td>4.525305</td>\n",
       "      <td>101.028770</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4126</th>\n",
       "      <td>Persiaran Tasik Botani (1 - 2)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restaurant Chap Heng</td>\n",
       "      <td>4.525305</td>\n",
       "      <td>101.028770</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4127</th>\n",
       "      <td>Persiaran Tasik Botani (1 - 2)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Falim 鱼旦仔粉饭档</td>\n",
       "      <td>4.525305</td>\n",
       "      <td>101.028770</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4128</th>\n",
       "      <td>Persiaran Tasik Botani (1 - 2)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Rainbow Seafood Restaurant</td>\n",
       "      <td>4.525305</td>\n",
       "      <td>101.028770</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4130</th>\n",
       "      <td>Persiaran Tasik Botani (1 - 2)</td>\n",
       "      <td>31350</td>\n",
       "      <td>天虹海鲜酒家</td>\n",
       "      <td>4.525305</td>\n",
       "      <td>101.028770</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4131</th>\n",
       "      <td>Persiaran Tasik Botani (1 - 2)</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restoran Wong Sheng 旺盛海鲜饭店</td>\n",
       "      <td>4.525305</td>\n",
       "      <td>101.028770</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4133</th>\n",
       "      <td>Pinggiran Rapat Ria</td>\n",
       "      <td>31350</td>\n",
       "      <td>Kopitiam Chee Kong</td>\n",
       "      <td>4.639720</td>\n",
       "      <td>101.130400</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4134</th>\n",
       "      <td>Pinggiran Rapat Ria</td>\n",
       "      <td>31350</td>\n",
       "      <td>Mee Tarik Warisan Asli</td>\n",
       "      <td>4.639720</td>\n",
       "      <td>101.130400</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4135</th>\n",
       "      <td>Ampang Baru</td>\n",
       "      <td>31350</td>\n",
       "      <td>Famous Jelapang Road Side Laksa And Fruit Rojak</td>\n",
       "      <td>4.621692</td>\n",
       "      <td>101.056269</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4195</th>\n",
       "      <td>Jalan Gopeng (118  - 211)</td>\n",
       "      <td>31350</td>\n",
       "      <td>南茶餐室</td>\n",
       "      <td>4.576583</td>\n",
       "      <td>101.076969</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4204</th>\n",
       "      <td>Jalan Lapangan Terbang</td>\n",
       "      <td>31350</td>\n",
       "      <td>Hong Kong Oil Chicken &amp; Roast Duck</td>\n",
       "      <td>4.568480</td>\n",
       "      <td>101.077010</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4226</th>\n",
       "      <td>Jalan Rokam</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restaurant Mee Fong</td>\n",
       "      <td>4.544486</td>\n",
       "      <td>101.067094</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4286</th>\n",
       "      <td>Lebuhraya Harilela</td>\n",
       "      <td>31350</td>\n",
       "      <td>KFG Claypot Chicken Rice</td>\n",
       "      <td>4.575243</td>\n",
       "      <td>101.070721</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4318</th>\n",
       "      <td>Palma D/1 - D/1A</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restaurant Michelin Star</td>\n",
       "      <td>4.246140</td>\n",
       "      <td>100.757340</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4319</th>\n",
       "      <td>Palma D/1 - D/1A</td>\n",
       "      <td>31350</td>\n",
       "      <td>群華海鮮圓酒家</td>\n",
       "      <td>4.246140</td>\n",
       "      <td>100.757340</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4320</th>\n",
       "      <td>Palma D/1 - D/1A</td>\n",
       "      <td>31350</td>\n",
       "      <td>新一色茶餐室 Restoran Sin Ek Sek</td>\n",
       "      <td>4.246140</td>\n",
       "      <td>100.757340</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4321</th>\n",
       "      <td>Palma D/1 - D/1A</td>\n",
       "      <td>31350</td>\n",
       "      <td>Kampung Koh Corner Mee Stall</td>\n",
       "      <td>4.246140</td>\n",
       "      <td>100.757340</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4322</th>\n",
       "      <td>Palma D/1 - D/1A</td>\n",
       "      <td>31350</td>\n",
       "      <td>Amu Coconut Villa Restaurant</td>\n",
       "      <td>4.246140</td>\n",
       "      <td>100.757340</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4323</th>\n",
       "      <td>Palma D/1 - D/1A</td>\n",
       "      <td>31350</td>\n",
       "      <td>新汉商酒楼 Restoran Sun Hon Siong</td>\n",
       "      <td>4.246140</td>\n",
       "      <td>100.757340</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4324</th>\n",
       "      <td>Palma D/1 - D/1A</td>\n",
       "      <td>31350</td>\n",
       "      <td>Restoran Ah Hing</td>\n",
       "      <td>4.246140</td>\n",
       "      <td>100.757340</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4325</th>\n",
       "      <td>Palma D/1 - D/1A</td>\n",
       "      <td>31350</td>\n",
       "      <td>富强板面</td>\n",
       "      <td>4.246140</td>\n",
       "      <td>100.757340</td>\n",
       "      <td>Chinese Restaurant</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                            Location  Postcode  \\\n",
       "4103             RPT Jaya Tambahan 2     31350   \n",
       "4104             RPT Jaya Tambahan 2     31350   \n",
       "4105        Jalan Palma (B/6 - B/15)     31350   \n",
       "4106        Jalan Palma (B/6 - B/15)     31350   \n",
       "4107        Jalan Palma (B/6 - B/15)     31350   \n",
       "4108         Jalan Rapat Ria (1 - 4)     31350   \n",
       "4109         Jalan Rapat Ria (1 - 4)     31350   \n",
       "4110         Jalan Rapat Ria (1 - 4)     31350   \n",
       "4111  Jalan Tasik Botani (A/1 - A/7)     31350   \n",
       "4112  Jalan Tasik Botani (A/1 - A/7)     31350   \n",
       "4113  Jalan Tasik Botani (A/1 - A/7)     31350   \n",
       "4115                Pengakalan Tiara     31350   \n",
       "4116                Pengakalan Tiara     31350   \n",
       "4118                Pengakalan Tiara     31350   \n",
       "4119                Pengakalan Tiara     31350   \n",
       "4120  Persiaran Tasik Botani (1 - 2)     31350   \n",
       "4125  Persiaran Tasik Botani (1 - 2)     31350   \n",
       "4126  Persiaran Tasik Botani (1 - 2)     31350   \n",
       "4127  Persiaran Tasik Botani (1 - 2)     31350   \n",
       "4128  Persiaran Tasik Botani (1 - 2)     31350   \n",
       "4130  Persiaran Tasik Botani (1 - 2)     31350   \n",
       "4131  Persiaran Tasik Botani (1 - 2)     31350   \n",
       "4133             Pinggiran Rapat Ria     31350   \n",
       "4134             Pinggiran Rapat Ria     31350   \n",
       "4135                     Ampang Baru     31350   \n",
       "4195       Jalan Gopeng (118  - 211)     31350   \n",
       "4204          Jalan Lapangan Terbang     31350   \n",
       "4226                     Jalan Rokam     31350   \n",
       "4286              Lebuhraya Harilela     31350   \n",
       "4318                Palma D/1 - D/1A     31350   \n",
       "4319                Palma D/1 - D/1A     31350   \n",
       "4320                Palma D/1 - D/1A     31350   \n",
       "4321                Palma D/1 - D/1A     31350   \n",
       "4322                Palma D/1 - D/1A     31350   \n",
       "4323                Palma D/1 - D/1A     31350   \n",
       "4324                Palma D/1 - D/1A     31350   \n",
       "4325                Palma D/1 - D/1A     31350   \n",
       "\n",
       "                                                 Name  Latitude   Longitude  \\\n",
       "4103                                            江沙牛肉面  4.800000  100.900000   \n",
       "4104                                         利民加地小食中心  4.800000  100.900000   \n",
       "4105                                      Kheng Hiong  4.415220  100.961750   \n",
       "4106                           Restoran Yin Fei 晏菲茶餐室  4.415220  100.961750   \n",
       "4107                      Restaurant Choy Pin (萍萍茶餐室)  4.415220  100.961750   \n",
       "4108                      Sam Ma Chicken Rice 三妈芽菜滑鸡饭  4.598570  101.119880   \n",
       "4109                              Yum Yum Bak Kut Teh  4.598570  101.119880   \n",
       "4110                 Restaurant Shion Mun Lau (常满楼饭店)  4.598570  101.119880   \n",
       "4111                                 Serdang易记海鲜档(炒粥)  5.161110  100.680440   \n",
       "4112              Restoran Bie You Tian 别有天海鲜 (咖哩山猪肉)  5.161110  100.680440   \n",
       "4113                           Sin Aik Kee Restaurant  5.161110  100.680440   \n",
       "4115                                            来发茶餐室  4.541907  101.072907   \n",
       "4116                           Restoran Fu Lim 富臨海鲜酒家  4.541907  101.072907   \n",
       "4118                                             文记饭店  4.541907  101.072907   \n",
       "4119                    Kedai Kopi You Like It 好锺意茶餐室  4.541907  101.072907   \n",
       "4120                              Restoran Ming Feong  4.525305  101.028770   \n",
       "4125                                            钻石咖喱粉  4.525305  101.028770   \n",
       "4126                             Restaurant Chap Heng  4.525305  101.028770   \n",
       "4127                                     Falim 鱼旦仔粉饭档  4.525305  101.028770   \n",
       "4128                       Rainbow Seafood Restaurant  4.525305  101.028770   \n",
       "4130                                           天虹海鲜酒家  4.525305  101.028770   \n",
       "4131                       Restoran Wong Sheng 旺盛海鲜饭店  4.525305  101.028770   \n",
       "4133                               Kopitiam Chee Kong  4.639720  101.130400   \n",
       "4134                           Mee Tarik Warisan Asli  4.639720  101.130400   \n",
       "4135  Famous Jelapang Road Side Laksa And Fruit Rojak  4.621692  101.056269   \n",
       "4195                                             南茶餐室  4.576583  101.076969   \n",
       "4204               Hong Kong Oil Chicken & Roast Duck  4.568480  101.077010   \n",
       "4226                              Restaurant Mee Fong  4.544486  101.067094   \n",
       "4286                         KFG Claypot Chicken Rice  4.575243  101.070721   \n",
       "4318                         Restaurant Michelin Star  4.246140  100.757340   \n",
       "4319                                          群華海鮮圓酒家  4.246140  100.757340   \n",
       "4320                       新一色茶餐室 Restoran Sin Ek Sek  4.246140  100.757340   \n",
       "4321                     Kampung Koh Corner Mee Stall  4.246140  100.757340   \n",
       "4322                     Amu Coconut Villa Restaurant  4.246140  100.757340   \n",
       "4323                     新汉商酒楼 Restoran Sun Hon Siong  4.246140  100.757340   \n",
       "4324                                 Restoran Ah Hing  4.246140  100.757340   \n",
       "4325                                             富强板面  4.246140  100.757340   \n",
       "\n",
       "                Category  \n",
       "4103  Chinese Restaurant  \n",
       "4104  Chinese Restaurant  \n",
       "4105  Chinese Restaurant  \n",
       "4106  Chinese Restaurant  \n",
       "4107  Chinese Restaurant  \n",
       "4108  Chinese Restaurant  \n",
       "4109  Chinese Restaurant  \n",
       "4110  Chinese Restaurant  \n",
       "4111  Chinese Restaurant  \n",
       "4112  Chinese Restaurant  \n",
       "4113  Chinese Restaurant  \n",
       "4115  Chinese Restaurant  \n",
       "4116  Chinese Restaurant  \n",
       "4118  Chinese Restaurant  \n",
       "4119  Chinese Restaurant  \n",
       "4120  Chinese Restaurant  \n",
       "4125  Chinese Restaurant  \n",
       "4126  Chinese Restaurant  \n",
       "4127  Chinese Restaurant  \n",
       "4128  Chinese Restaurant  \n",
       "4130  Chinese Restaurant  \n",
       "4131  Chinese Restaurant  \n",
       "4133  Chinese Restaurant  \n",
       "4134  Chinese Restaurant  \n",
       "4135  Chinese Restaurant  \n",
       "4195  Chinese Restaurant  \n",
       "4204  Chinese Restaurant  \n",
       "4226  Chinese Restaurant  \n",
       "4286  Chinese Restaurant  \n",
       "4318  Chinese Restaurant  \n",
       "4319  Chinese Restaurant  \n",
       "4320  Chinese Restaurant  \n",
       "4321  Chinese Restaurant  \n",
       "4322  Chinese Restaurant  \n",
       "4323  Chinese Restaurant  \n",
       "4324  Chinese Restaurant  \n",
       "4325  Chinese Restaurant  "
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "top5_df[top5_df['Postcode'] == 31350]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# POPULATION DATA\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Additionally lets take a look at the Population by Ethnicity of Ipoh\n",
    "\n",
    "\n",
    "According to Malaysia'Censur Information: https://web.archive.org/web/20120227011347/http://www.statistics.gov.my/portal/download_Population/files/population/04Jadual_PBT_negeri/PBT_Perak.pdf\n",
    "The Population of Ipoh stands at 828,000"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Lets collect some data for a better view "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Ethnicity</th>\n",
       "      <th>Population</th>\n",
       "      <th>Percentage</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Chinese</td>\n",
       "      <td>290165</td>\n",
       "      <td>44.11</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Bumiputera</td>\n",
       "      <td>253592</td>\n",
       "      <td>38.55</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Indian</td>\n",
       "      <td>92587</td>\n",
       "      <td>14.07</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Others</td>\n",
       "      <td>1559</td>\n",
       "      <td>0.20</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>Non-Malaysian</td>\n",
       "      <td>19989</td>\n",
       "      <td>3.04</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       Ethnicity  Population  Percentage\n",
       "0        Chinese      290165       44.11\n",
       "1     Bumiputera      253592       38.55\n",
       "2         Indian       92587       14.07\n",
       "3         Others        1559        0.20\n",
       "4  Non-Malaysian       19989        3.04"
      ]
     },
     "execution_count": 32,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "eth_df = pd.read_csv('Ethnicity Group.csv')\n",
    "eth_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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rWnJ9u3bAQBXXXVVi7cbDIZmHXrMRFG07LGat2dmPhaak5PT6rZ///33Vm9rjfn+wsLCWm2eMz+mlpg739m7p+Go57Wr5eTkID09vcXbKisrceTIEQDNXzczc6fLb775Bvn5+ZapwuVsjTDvYcmxl9hZY8aMgbe3NwBg8+bNDrvfjryfg4KCMHfuXADSYSpzfwlfX18sWLDAYTXZasKECQCAH374ocOda8ePHw9A2oNubQK6traZm5vb6vdaV7Ll9TJ/x8XFxbXav6K177jRo0dbPidtncittdvGjx9vWb87daD3dLIFiREjRmDIkCEAgBdffLHF0Qtbt261/Jibv2Ba8s9//rNZJx8A+OyzzywzwN15551Wt40cORKANJNdS2Hi5MmTlt7BHWHunW3u3d/U+fPn8fbbb7e6fmBgIABY9a/oCEc+r13thRdeaPH61157DbW1tVCpVLjttttaXGbixIkYNmwY6urqcOedd6KoqKjTnSw7q7OvnZz8/Pxw1113AZCa8tsK2B3R0efEHBC/++47ywymd955Z6c6Wdpr8eLFEAQBZWVleOyxx9pcVq/XW4WN/v3747rrrgMgjc6pqKiwaZuzZ8+2tGY8/PDD7R7fb60zrr1seb3M33FpaWkttugmJSXhq6++anHd4OBgy6Hu1157zdJptLE9e/a02NESkFo0zKNOXn31VaSlpbXxaBz//FDLZAsSAPCvf/0LALB3717MmTMHGRkZAKQP5erVqy0/cuPHj7cMsWrKz88P+/btw7x58yzN5XV1dfj4448tX0q33HKLZbij2ezZsxEQEAC9Xo877rgDp0+ftmz7+++/x9SpUzvUScps4sSJ8Pf3hyiKuOOOOyxvdKPRiG3btiE+Pr7NY4PDhg0DAFRUVGDdunUd3j7gmOe1qwUFBeGzzz7Dww8/bOl4WllZiZdeeskSMP7617+22SnT3NxtbnWSu5Ol+bVbvXq1S3bw+uc//4nQ0FAUFxdjwoQJWLdunaUzX319PY4dO4bHHnsMX3zxhc33aX5Otm7d2uq0342ZD001NDRYwq5crUyjRo2ynIH3gw8+wO23346kpCTL3rrRaERycjJeeOEF9OvXD0lJSVbrv/XWW1Cr1Thz5gwmTJiAn376ydK5saamBr///jseeOABq713tVqN9957D4Ig4OjRo5gwYQK2bdtm9YOb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\n",
      "text/plain": [
       "<Figure size 540x540 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(6,6),dpi= 90,facecolor='w')\n",
    "plt.title('Population by Ethnicity Pecentage',fontsize= 20,pad=30)\n",
    "sizes = eth_df['Percentage']\n",
    "labels = eth_df['Ethnicity']\n",
    "explode = (0.05, 0.05, 0.05, 0.05, 0.05)\n",
    "colors = ['#ff9999','#66b3ff','#99ff99','#E2A8FE','#ffcc99']\n",
    "plt.pie(sizes, labels=labels, explode=explode,colors=colors, autopct='%1.0f%%', shadow=True)\n",
    "# Draw circle\n",
    "centre_circle = plt.Circle((0,0),0.70,fc='white')\n",
    "fig = plt.gcf()\n",
    "fig.gca().add_artist(centre_circle)\n",
    "# Equal aspect ratio ensures that pie is drawn as a circle\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "From this we could clearly see that majority of the population in Ipoh are chinese, hence the market for chinese resturant has a great potential"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}