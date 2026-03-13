import streamlit as st
import cv2
import numpy as np
import pandas as pd
import re
import random
import easyocr
import sqlite3
import os
import plotly.express as px
from datetime import datetime
from reportlab.pdfgen import canvas
from streamlit_autorefresh import st_autorefresh
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="TRANSPORT-PANIMALAR",
    page_icon="🚌",
    layout="wide"
)

# ---------------------------------------------------
# LOADING ANIMATION
# ---------------------------------------------------

with st.spinner("🚍 Initializing PANIMALAR Transport System... Developed By Dept Of ADS "):
    time.sleep(3)

# ---------------------------------------------------
# HEADER STYLE
# ---------------------------------------------------
st.markdown("""
<style>

.main-header{
font-size:38px;
font-weight:700;
background: linear-gradient(90deg,#00c6ff,#0072ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.status-arrived{
color:white;
background:#28a745;
padding:6px 14px;
border-radius:20px;
animation:pulse 2s infinite;
}

.status-pending{
color:white;
background:#dc3545;
padding:6px 14px;
border-radius:20px;
}

@keyframes pulse {
0% {transform: scale(1);}
50% {transform: scale(1.05);}
100% {transform: scale(1);}
}

</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# LOGO + TITLE
# ---------------------------------------------------

col1, col2 = st.columns([1,6])

with col1:
    st.image("logo.png", width=90)

with col2:
    st.markdown('<div class="main-header">TRANSPORT‑PANIMALAR</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# LOGIN SESSION
# ---------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

PASSWORD = "busadmin123"

# ---------------------------------------------------
# OCR
# ---------------------------------------------------

reader = easyocr.Reader(['en'])

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

conn = sqlite3.connect("bus_system.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS buses(
plate TEXT PRIMARY KEY,
bus_name TEXT,
route TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS entries(
token INTEGER,
plate TEXT,
bus TEXT,
route TEXT,
time TEXT,
date TEXT
)
""")

conn.commit()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
"Go to",
["Dashboard","Capture Bus","Manage Buses","Reports"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False

# ---------------------------------------------------
# PLATE EXTRACTOR
# ---------------------------------------------------

def extract_plate(texts):

    combined="".join(texts)
    combined=combined.upper()

    combined=re.sub(r'[^A-Z0-9]','',combined)

    pattern=r'TN[0-9]{1,2}[A-Z]{0,2}[0-9]{3,4}'

    match=re.search(pattern,combined)

    if match:
        return match.group()

    return None

# ---------------------------------------------------
# PDF REPORT
# ---------------------------------------------------

def generate_daily_report(entries):

    today=datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename=f"reports/bus_report_{today}.pdf"

    c=canvas.Canvas(filename)

    c.drawString(100,800,f"Bus Arrival Report - {today}")

    y=760

    for index,row in entries.iterrows():

        text=f"{row['token']} {row['plate']} {row['bus']} Route:{row['route']} {row['time']}"

        c.drawString(100,y,text)

        y-=20

    c.save()

    return filename

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
st.caption("AI Powered Bus Arrival Detection System")
st.caption("PANIMALAR ENGINEERING COLLEGE  - CHENNAI")
if menu=="Dashboard":

    # Smaller centered bus image
    colA,colB,colC = st.columns([1,2,1])

    with colB:
        if os.path.exists("panimalar.jpg"):
            st.image("panimalar.jpg", width=750)

    st_autorefresh(interval=5000, key="dashboard_refresh")

    buses=pd.read_sql("SELECT * FROM buses",conn)
    entries=pd.read_sql("SELECT * FROM entries",conn)

    total=len(buses)
    arrived=len(entries)
    pending=total-arrived

    c1,c2,c3=st.columns(3)

    c1.metric("Total Buses",total)
    c2.metric("Arrived Today",arrived)
    c3.metric("Pending",pending)

    st.divider()

    if not entries.empty:

        last=entries.iloc[-1]

        st.info(f"Last Bus Arrived: {last['bus']} ({last['plate']}) Route {last['route']} at {last['time']}")

    st.subheader("Arrival Log")

    st.dataframe(entries,use_container_width=True)

    st.subheader("Arrival Board")

    board=[]

    for index,row in buses.iterrows():

        plate=row["plate"]
        bus=row["bus_name"]
        route=row["route"]

        match=entries[entries["plate"]==plate]

        if not match.empty:

            status="<span class='status-arrived'>Arrived</span>"
            time=match.iloc[-1]["time"]

        else:

            status="<span class='status-pending'>Pending</span>"
            time="-"

        board.append({
        "Bus":bus,
        "Route":route,
        "Plate":plate,
        "Status":status,
        "Time":time
        })

    board_df=pd.DataFrame(board)

    st.write(board_df.to_html(escape=False),unsafe_allow_html=True)

# ---------------------------------------------------
# CAPTURE BUS
# ---------------------------------------------------

if menu=="Capture Bus":

    if not st.session_state.logged_in:

        st.title("Login Required")

        password=st.text_input("Password",type="password")

        if st.button("Login"):

            if password==PASSWORD:

                st.session_state.logged_in=True
                st.success("Login Successful")

            else:

                st.error("Wrong Password")

    else:

        st.title("Capture Bus Plate")

        image=st.camera_input("Scan Number Plate")

        if image:

            file_bytes=np.asarray(bytearray(image.read()),dtype=np.uint8)
            img=cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)

            img=cv2.resize(img,None,fx=2,fy=2)

            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            gray=cv2.equalizeHist(gray)

            blur=cv2.bilateralFilter(gray,11,17,17)

            thresh=cv2.adaptiveThreshold(
                blur,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )

            result=reader.readtext(thresh)

            texts=[d[1] for d in result]

            st.write("OCR Text:",texts)

            plate=extract_plate(texts)

            st.write("Detected Plate:",plate)

            if plate:

                bus=pd.read_sql(
                f"SELECT * FROM buses WHERE plate='{plate}'",
                conn
                )

                if not bus.empty:

                    token=random.randint(10000,99999)

                    bus_name=bus.iloc[0]["bus_name"]
                    route=bus.iloc[0]["route"]

                    now=datetime.now()

                    time=now.strftime("%H:%M:%S")
                    date=now.strftime("%Y-%m-%d")

                    cursor.execute(
                    "INSERT INTO entries VALUES (?,?,?,?,?,?)",
                    (token,plate,bus_name,route,time,date)
                    )

                    conn.commit()

                    st.success("Bus Entry Recorded")

                else:

                    st.error("Bus not found in database")

            else:

                st.warning("No plate detected")

# ---------------------------------------------------
# MANAGE BUSES
# ---------------------------------------------------

if menu=="Manage Buses":

    if not st.session_state.logged_in:

        st.title("Admin Login")

        password=st.text_input("Password",type="password")

        if st.button("Login"):

            if password==PASSWORD:

                st.session_state.logged_in=True
                st.success("Login Successful")

            else:

                st.error("Wrong Password")

    else:

        st.title("Add Bus")

        name=st.text_input("Bus Name")
        plate=st.text_input("Plate Number")
        route=st.text_input("Route Number")

        if st.button("Add Bus"):

            cursor.execute(
            "INSERT INTO buses VALUES(?,?,?)",
            (plate,name,route)
            )

            conn.commit()

            st.success("Bus Added")

        buses=pd.read_sql("SELECT * FROM buses",conn)

        st.subheader("Bus Database")

        st.dataframe(buses,use_container_width=True)

        st.subheader("Delete Bus")

        delete_plate=st.selectbox(
        "Select Bus Plate",
        buses["plate"]
        )

        if st.button("Delete Bus"):

            cursor.execute(
            "DELETE FROM buses WHERE plate=?",
            (delete_plate,)
            )

            conn.commit()

            st.warning("Bus Deleted")

# ---------------------------------------------------
# REPORT PAGE
# ---------------------------------------------------

if menu=="Reports":

    st.title("Reports")

    entries=pd.read_sql("SELECT * FROM entries",conn)

    st.dataframe(entries)

    csv=entries.to_csv(index=False)

    st.download_button(
    "Download CSV",
    csv,
    "bus_report.csv"
    )

    report=generate_daily_report(entries)

    with open(report,"rb") as file:

        st.download_button(
        "Download Today's PDF",
        file,
        file_name=report,
        mime="application/pdf"
        )