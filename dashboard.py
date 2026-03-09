import streamlit as st
import pandas as pd
import pydeck as pdk 
import matplotlib.pyplot as plt 

#desain halaman
st.set_page_config(page_title="E-Commspatial Dashboard", layout="wide")
st.header('**E-Commerspatial Dashboard By Putri :world_map:**')
st.write("analisis sebaran pelanggan & top 5 negara bagian dengan pelanggan e-commerce terbanyak")

#load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    #renamde koordinat
    df = df.rename(columns={
        "geolocation_lat": "lat",
        "geolocation_lng": "lon",
    })
    return df
df = load_data()

#pemetaan negara bagian
state_mapping = {
    "SP" : "Sao Paulo",
    "RJ" : "Rio de Janiero",
    "MG" : "Minas Gerais",
    "RS" : "Rio Grande do suol",
    "PR" : "Parana",
}
df["state_full"] = df["customer_state"].map(state_mapping)
df["state_full"] = df["state_full"].fillna(df["customer_state"])
df["state_full"] = df["state_full"].astype(str)

#5 negara bagian teratas jumlah pelanggan
top5 = (
    df["state_full"]
    .value_counts()
    .head(5)
    .reset_index()
)
top5.columns = ["negara bagian", "jumlah pelanggan"]

total_all_customers = df["customer_id"].nunique()
top_state_count = top5["jumlah pelanggan"].iloc[0]
top_state_name = top5["negara bagian"].iloc[0]
proportion = (top_state_count / total_all_customers) * 100
st.subheader(' analisis distribusi pelanggan utama :bar_cchart')

col1, col2 = st.columns(2)
with col1:
     st.metric(label='total pelanggann', value=f"{total_all_customers:,}")
     st.metric(label=f"Dominasi {top_state_name}", value=f"{proportion:.2f}%")
with col2:
    fig, ax = plt.subplots()
    ax.barh(top5["negara bagian"],
top5["jumlah pelanggan"])
    ax.set_xlabel("jumlah pelanggan")
    ax.set_title("top 5 customer distribution")
    ax.invert_yaxis()
    st.pyplot(fig)
st.divider()

#filtering sidebar
st.sidebar.header("filter peta")
state_list = sorted(df["state_full"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "pilih negra bagian:",
    options=state_list,
    default=top5["negara bagian"].tolist()
)
filtered_df = df[df["state_full"].isin(selected_states)]

#data peta
map_df = filtered_df.dropna(subset=["lat","lon"]).copy()
map_df.loc["lat"] = pd.to_numeric(map_df["lat"], errors="coerce")
map_df.loc["lng"] = pd.to_numeric(map_df["lon"], errors="coerce")

map_df = map_df.dropna(subset=["lat", "lon"])

#peta
st.subheader("sebaran Pelanggan E-Commerce")

map_df = filtered_df.dropna(subset=['lat', 'lon']).copy()
map_df['lat'] = pd.to_numeric(map_df["lat"], errors="coerce")
map_df['lon'] = pd.to_numeric(map_df["lon"], errors="coerce")
map_df = map_df.dropna(subset=["lat", "lon"])

if not map_df.empty:
    st.map(map_df[["lat", "lon"]])
else:
    st.warning("silahkan pilih wilayahnya di sidebar")


