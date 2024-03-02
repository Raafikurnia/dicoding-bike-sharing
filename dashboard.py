import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#create_monthly_user_df()
def create_monthly_user_df(df):
    monthly_user_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_user_df.index = monthly_user_df.index.strftime('%b-%y')
    monthly_user_df = monthly_user_df.reset_index()
    monthly_user_df.rename(columns={
        "dteday": "tahun-bulan",
        "casual": "peminjam_casual",
        "registered": "peminjam_registered",
        "cnt": "total_peminjam"
    }, inplace=True)
        
    return monthly_user_df

#create_byseason_df()
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").agg({
       "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    byseason_df = byseason_df.reset_index()
    byseason_df.rename(columns={
        "casual": "peminjam_casual",
        "registered": "peminjam_registered",
        "cnt": "total_peminjam"
    }, inplace=True)

    byseason_df=pd.melt(byseason_df, id_vars=['season'], value_vars=['peminjam_casual', 'peminjam_registered'], var_name='tipe_peminjam', value_name='count_rides')  
    byseason_df['season']=pd.Categorical(byseason_df['season'], categories=['Spring', 'Summer', 'Winter', 'Autumn'])
    byseason_df=byseason_df.sort_values('season')
    return byseason_df

#create_byweekday_df()
def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday").agg({
       "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    byweekday_df = byweekday_df.reset_index()
    byweekday_df.rename(columns={
        "casual": "peminjam_casual",
        "registered": "peminjam_registered",
        "cnt": "total_peminjam"
    }, inplace=True)

    byweekday_df=pd.melt(byweekday_df, id_vars=['weekday'], value_vars=['peminjam_casual', 'peminjam_registered'], var_name='tipe_peminjam', value_name='count_rides')  
    byweekday_df['weekday']=pd.Categorical(byweekday_df['weekday'], categories=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    byweekday_df=byweekday_df.sort_values('weekday')
    return byweekday_df



#Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/Raafikurnia/dicoding-bike-sharing/main/day_df.csv")
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

#Komponen filter
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo
    st.image("https://github.com/Raafikurnia/dicoding-bike-sharing/raw/main/bike.png")
        
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
    
monthly_user_df = create_monthly_user_df(main_df)
byseason_df = create_byseason_df(main_df)
byweekday_df= create_byweekday_df(main_df)
#rfm_df = create_rfm_df(main_df)

st.header('Bike Shared Dashboard :sparkles:')

st.subheader('Tipe Peminjam')
col1, col2 = st.columns(2)
with col1:
    total_casual = main_df['casual'].sum()
    st.metric("Total Peminjam Casual", value=total_casual)
 
with col2:
    total_registered = main_df['registered'].sum()
    st.metric("Total Peminjam Registered", value=total_registered)

st.subheader('Total Peminjam')
total_seluruh = main_df['cnt'].sum()
st.metric("Total Keseluruhan", value=total_seluruh)


st.subheader("Performa")
day_df['month_year'] = day_df['dteday'].dt.strftime('%B %Y')
day_df['month_year'] = pd.Categorical(day_df['month_year'], categories=day_df['month_year'].unique(), ordered=True)

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="month_year", y="cnt", data=day_df)
plt.xlabel("Date")
plt.ylabel("Total Peminjaman")
plt.title("Performa")
plt.xticks(rotation=45) 
plt.tight_layout()
st.pyplot(fig)


st.subheader("Sebaran Peminjaman berdasarkan Musim dan Hari")
     
col1, col2 = st.columns(2)
     
with col1:
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x="season", y="cnt", data = day_df)  
    plt.xlabel("Season")
    plt.ylabel("Total")
    plt.title("Total Peminjaman Berdasarkan Season")

    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(x="weekday", y="cnt", data = day_df)  
    plt.xlabel("Weekday")
    plt.ylabel("Total")
    plt.title("Total Peminjaman Berdasarkan Hari")

    st.pyplot(fig)

st.caption('Copyright (c) Dicoding-Raafi 2024')

  
