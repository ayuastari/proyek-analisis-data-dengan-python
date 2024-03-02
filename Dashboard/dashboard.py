import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

day_df  = pd.read_csv('https://raw.githubusercontent.com/ayuastari/proyek-analisis-data-dengan-python/main/dataset/day.csv')
day_df.head()

#Cleaning Data
#Menghapus(drop) kolom yang tidak diperlukan
drop_column = ["instant", "hum", "windspeed"]

for n in day_df.columns:
  if n in drop_column:
   day_df.drop(labels=n, axis=1, inplace=True)

#Mengubah nama data menjadi nama yang mudah dipahami
day_df.rename(columns = {
    "dteday":"dateday",
    "yr":"year",
    "mnth":"month",
    "cnt":"count",
}, inplace=True)

#Memberikan keterangan
day_df["year"]= day_df["year"].map({0:2011, 1:2012})
day_df["month"]= day_df["month"].map({1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"june", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"})
day_df["weekday"]= day_df["weekday"].map({0:"Sunday",1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday"})
day_df["season"]= day_df["season"].map({1:"spring", 2:"summer", 3:"fall", 4:"winter"})
day_df["weathersit"]= day_df["weathersit"].map({1:"Clear, Few clouds, Partly cloudy, Partly cloudy", 2:"Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist", 3:"Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds", 4:"Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"})
day_df.head()

#membuat beberapa helper function untuk menyiapkan rent dari daily hingga holiday
def create_daily_df(df):
 daily_rent_df = day_df.groupby(by=['dateday','year']).agg({
       'temp':'sum',
       'count': 'sum'}).reset_index()
 return daily_rent_df

def create_casual_df(df):
 casual_rent_df = day_df.groupby(by='dateday').agg({'casual': 'sum'}).reset_index()
 return casual_rent_df

def create_registered_df(df):
 registered_rent_df = day_df.groupby(by='dateday').agg({ 'registered': 'sum'}).reset_index()
 return registered_rent_df

def create_season_df(df):
 season_rent_df = day_df.groupby(by="season").agg({
      "count" : "sum",
      "workingday" : "sum",
      "holiday" :"sum"}).reset_index()
 return season_rent_df

def create_weekday_df(df):
 weekday_rent_df = day_df.groupby(by=['weekday','year']).agg({'count':'sum'}).reset_index()
 return weekday_rent_df

def create_workingday_df(df):
 workingday_rent_df = day_df.groupby(by=['workingday','season']).agg({
    'count':'sum',
    'registered':'sum',
    'casual':'sum'}).reset_index()
 return workingday_rent_df

def create_holiday_df(df):
 holiday_rent_df = day_df.groupby(by="holiday").agg({
  "count":"sum"}).reset_index()
 return holiday_rent_df

#Membuat komponen filter
min_date = pd.to_datetime(day_df["dateday"]).dt.date.min()
max_date = pd.to_datetime(day_df["dateday"]).dt.date.max()

with st.sidebar:
 st.title("Bike Sharing")
 st.image("https://raw.githubusercontent.com/ayuastari/proyek-analisis-data-dengan-python/main/Dashboard/bicycle.jpg")
 start_date, end_date = st.date_input(
   label="Time",
   min_value=min_date,
   max_value=max_date,
   value=[min_date,max_date]
)
 
date_df=day_df[(day_df["dateday"]>=str(start_date)) & 
               (day_df["dateday"]>=str(end_date))]

#Data Frame
daily_rent_df= create_daily_df(date_df)
registered_rent_df = create_registered_df(date_df)
casual_rent_df = create_casual_df(date_df)
season_rent_df = create_season_df(date_df)
weekday_rent_df = create_weekday_df(date_df)
workingday_rent_df = create_workingday_df(date_df)
holiday_rent_df = create_holiday_df(date_df)

#Dashboard
st.title(":bicyclist: Bike Sharing Dashboard :bicyclist:")
col1, col2, col3 = st.columns(3)

with col1:
    rent_daily_total = daily_rent_df["count"].sum()
    st.metric("Total Users", value = rent_daily_total)
with col2: 
    rent_casual_total = casual_rent_df["casual"].sum()
    st.metric("Casual Users", value = rent_casual_total)
with col3:
    rent_registered = registered_rent_df["registered"].sum()
    st.metric("Registered Users", value = rent_registered)

#bike sharing on every season
col = st.columns((1.5,6),gap="small") 
with col[1]:  
  st.subheader("Bike Sharing in Season")
  fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20,5))

 # Bar plot for workingday
  sns.barplot(
    x='season',
    y='workingday',
    data=season_rent_df,
    hue='season',
    palette='viridis',
    ax=ax[0],
    )
  ax[0].set_xlabel('Seasons', fontsize=12)
  ax[0].set_ylabel('Total Workingday', fontsize=12)
  ax[0].set_title('Comparison of Total Workingdays between Seasons', fontsize=20)

 # Bar plot for holiday
  sns.barplot(
    x='season',
    y='holiday',
    data=season_rent_df,
    hue='season',
    palette='viridis',
    ax=ax[1],
 )
  ax[1].set_xlabel("Seasons", fontsize=12)
  ax[1].set_ylabel("Total Holiday", fontsize=12)
  ax[1].set_title("Comparison of Total holidays between Seasons", loc="center", fontsize=20)
  st.pyplot(fig)
 
  st.markdown("---")

 #Grafic of bike users by temperature
  st.subheader("Bike Sharing in Temperature for 2 years")  
  fig, ax=plt.subplots(figsize=(30,5))
  colors= plt.get_cmap("viridis")

  sns.scatterplot(
    x="dateday",
    y="temp",
    hue="count",
    data=daily_rent_df,
    palette=colors,
    ax=ax
 )

  ax.set_title("Relationship between Temperature and Total Count of Bicycle Users for Each Season in a Time Span of 2 Years", loc="center", fontsize=30)
  ax.set_xlabel("Time Span", fontsize=20)
  ax.set_ylabel("Temperature", fontsize=20)
  st.pyplot(fig)

  st.markdown("---")
 #Bike user in a weeks for two years
  st.subheader("Bike Sharing in Weekday for 2 years")
  fig, ax = plt.subplots(figsize=(15,5))
  colors_ = ["#006400", "#00008B"]

  sns.lineplot(
  x="weekday",
  y="count",
  hue="year",
  data=weekday_rent_df,
  palette=colors_,
  marker="o"
 )

  ax.set_title("Average Weekly Bike Users in 2 Years", loc="center", fontsize=30)
  ax.set_xlabel("Day", fontsize=20)
  ax.set_ylabel("Total Bikes", fontsize=20)
  st.pyplot(fig)

  st.caption('Copyright © 2024')