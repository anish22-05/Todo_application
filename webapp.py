# import streamlit as st
# import requests
# from streamlit_js_eval import get_geolocation

# #---------Config & Style----------------------------------
# st.set_page_config(page_title="Obiwan Todo",layout = "wide")

# st.markdown("""
#     <style>
#         .main {background-color: #f5f7f9;}
#         .stButton>button {border-radius: 20px; width: 100%; }
#         .task_card {pending: 15px; border-radius: 10px; background: white; margine-bottom: 10px; border-left: 5px solid #4CAF50; }
#         </style>
# """, unsafe_allow_html=True)
# # --------GEt Location & Weather -------
# col1, col2 = st.columns([2,1])
# # with col2:
# #     st.subheader("Context")
# #     location = get_geolocation()
# #     if location:
# #         lat = location['coords']['latitude']
# #         lon = location['coords']['longitude']

# #         # weather api
# #         w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=ture"
# #         w_res = requests.get(w_url).json()
# #         # temp  = w_res['current_weather']['temperature']
# #         # w_code = w_res['current_weather']['weathercode']
# #         # st.metric("Temperature", f"{temp}")
# #         # st.write(f"Coords: {round(lat,2)},{round(lon,2)}")
# #         # current_weather = "Clear" if w_code < 3 else "Cloudy/Rainy"
# #         if 'current_weather' in w_res:
# #             temp = w_res['current_weather']['temperature']
# #             w_code = w_res['current_weather']['weathercode']
# #             st.metric("Temperature",f"{temp}°C")
# #             st.write(f"Coords: {round(lat,2)}, {round(lon,2)}")

# #     else:
# #         st.info("Allow location access to sync weather.")
# #         current_weather="Unknown"
# #         lat, lon = None, None
# with col2:
#     st.subheader("Current Context")
#     location = get_geolocation()
    
#     if location:
#         lat = location['coords']['latitude']
#         lon = location['coords']['longitude']
# #-----------the logic for this weather and location is shifted to api so we dont need it now---------------------
#         # # Ask the Nomination database for the address for above cordinates
#         # geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
#         # # User-Agent is just a required 'ID' so they dont block you
#         # geo_res = requests.get(geo_url, headers={"User-Agent": "MyTodoApp"}).json()
#         # # Extract the name (city, town or village)
#         # address = geo_res.get('address',{})
#         # loc_name = address.get('city') or address.get('town') or address.get('village') or "Unknown"
#         # #Display it
#         # st.write(f" **{loc_name}** ({lat},{lon})")
        
#     #     # 2. FIXED: Changed 'ture' to 'true'
#     #     w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
#     #     w_res = requests.get(w_url).json()

#     #     if 'current_weather' in w_res:
#     #         temp = w_res['current_weather']['temperature']
#     #         w_code = w_res['current_weather']['weathercode']
            
#     #         # 3. Create the text description for your task database
#     #         current_weather = "Clear" if w_code < 3 else "Cloudy/Rainy"
            
#     #         st.metric("Temperature", f"{temp}°C")
#     #         st.caption(f"Sky: {current_weather}") # Shows the status nicely
#     #         st.write(f"Coords: {round(lat,2)}, {round(lon,2)}")
#     # else:
#     #     st.info("Allow location access to sync weather.")
#         ctx = requests.get(f"http://127.0.0.1:8000/tasks/context?lat={lat}&lon={lon}").json()
#         st.metric("Temp",f"{ctx['temperature']}°C")
#         st.write(f"{ctx['location_name']}")

# #--------Fetch & Filter Tasks
# with col1:
#     st.title("My Modern Tasks")
#     # Connect to your FastAPI Backend
#     try:
#         api_url = "http://127.0.0.1:8000/tasks/"
#         response = requests.get(api_url)
#         all_tasks = response.json()
#         # we will show tasks that are not yet completed
#         active_tasks = [t for t in all_tasks if not t['completed']]
#         if not active_tasks:
#             st.success("All caught up!")
#         for task in active_tasks:
#             with st.container():
#                 c1, c2, c3 = st.column([3,1,1])
#                 c1.markdown(f"**{task['title']}** \n*{task['category']}*")
#                 c2.write(f"{task['duration']}m")
#                 if c3.button("Complete",key=task['id']):
#                     requests.patch(f"{api_url}{task['id']}/archive")
#                     st.rerun()
#                 st.divider()
#     except Exception as e:
#         st.error("Could not connect to Backend Api.")
# # Add task---------------
# with st.sidebar:
#     st.header("Quick Add")
#     with st.form("new_task"):
#         new_title = st.text_input("Task_Title")
#         new_cat = st.selectbox("Category",["Home","Errand","Work"])
#         submit = st.form_submit_button("Add Task")
#         if submit and new_title:
#             payload= {
#                 "title":new_title,
#                 "category": new_cat,
#                 "location": str(location) if location else "Local",
#                 "weather": current_weather,
#                 "completed": False
#             }
#             requests.post(api_url, json=payload)
#             st.rerun()

import streamlit as st
import requests
from streamlit_js_eval import get_geolocation
from datetime import datetime

st.set_page_config(page_title = "Distributed Todo", layout="wide")
st.markdown("""
            <style>
                .main {background-color: #f5f7f9;}
                .stButton>button {border-radius: 20px; width: 100%;transition: 0.3s;}
                .stButton>button:hover {background-color: #4CAF50; color: white;}
                .intelligence-card{
                    padding: 20px;
                    border-radius: 15px;
                    background: #e1f5fe;
                    color: #01579b;
                    border-left: 10px solid #0288d1;
                    margin-bottom: 20px;
                    line-height: 1.6;
                    box-shadow: 0 4px 6px -1px rgbs(0,0,0,0.1);
                    font-family: sans-serif;
                }
                .intelligence-card h3 {color: #1e3a8a !important; margin-top: 0;}
                .context-box{
                            padding: 15px; 
                            border-radius: 12px; 
                            background: #fdf5e6; 
                            margin-bottom: 10px; 
                            border: 1px solid #e1d4bb; 
                            box-shadow: 4px 4px 10px rgba(0,0,0,0.08);
                            color: #4a4432;
                            line-height: 1.5;
                            }
            </style>
            """,unsafe_allow_html=True)
BASE_URL = "http://127.0.0.1:8000"
API_BASE_URL = f"{BASE_URL}/tasks"
#--------------get api data function will avoid repeated try andexcept logic
def get_api_data(url, params=None):
    try:
        res = requests.get(url,params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return None
     
#--------------------------layout for app
col1, col2 = st.columns([2,1])
# Initilaize global state variables so the Add Task from doesn't crash
current_weather = "Unknown"
location_label = "Local"
is_connected = False
with col2:
    st.subheader("Current Context")
    location = get_geolocation()
    if location:
        lat = location['coords']['latitude']
        lon = location['coords']['longitude']
        ctx_url = f"{BASE_URL}/context"
        ctx = get_api_data(ctx_url,{"lat": lat,"lon": lon})
        if ctx:
            #-----Mapping data from services.py---------
            is_connected = True
            # temp = ctx.get('temperature', 'N/A')
            location_label = ctx.get('location_name','Unknown')
            current_weather = ctx.get('weather_condition','Unknown')
            local_time = ctx.get('local_time_str','N/A')
            temp = ctx.get('temperature','N/A')
            local_date = ctx.get('local_date','N/A')

            st.markdown(f"""
                    <div class = "context-box">
                        <strong> Location:</strong> {location_label}<br>
                        <strong> Temperature:</strong> {temp}C<br>
                        <strong> Date:</strong> {local_date}<br>
                        <strong> Local Time: </strong> {local_time}<br>
                        <strong> Weather: </strong> {current_weather}
                    </div>
            """, unsafe_allow_html=True)
            # Fetch Agent Intelligence
            st.divider()
            st.subheader("Agent Console")
            with st.expander("System Intelligence",expanded=True):
                quick_params = {"lat":lat,"lon":lon,"use_llm":False}
                quick_intel = get_api_data(f"{BASE_URL}/intelligence",params=quick_params)
                if quick_intel:
                    st.write(quick_intel.get("intelligence_report","Analyzing tasks..."))

            #--Create button to run llm on button click
            if st.button("Assistance from llm."):
                with st.spinner("LLM is analyzing ..."):
                # The backend run method defaults to use llm=True
                # backend main file calls agent_master.run to use openai
                    llm_params =  {"lat": lat, "lon":lon, "use_llm": True}
                    intel = get_api_data(f'{BASE_URL}/intelligence', params = llm_params)
                    if intel and "intelligence_report" in intel:
                        st.markdown(f"""<div class="intelligence-card">
                                        <h3> LLM's Opiniom</h3>
                                        {intel['intelligence_report']}
                                    </div>""", unsafe_allow_html=True)        
        else:
            st.warning("Backend Connection Failed, We'r Offline.")
    else:
        st.info("Please allow location access in your browser")
#----------Task Display Logic----------------
with col1:
    st.title("My Obligations:")
    all_tasks = get_api_data(API_BASE_URL)
    if all_tasks is not None:
        # looking for active tasks. id will be integer value.
        active_tasks = [t for t in all_tasks if not t.get('completed')]
        if not active_tasks:
            st.success("All caught up and Complete.")
        for task in active_tasks:
            with st.container():
                c1,c2,c3 = st.columns([3,1,1])
                with c1:
                    st.markdown(f"**{task['title']}**")
                    st.caption(f"{task.get('category')} * {task.get('priority')} * {task.get('location')}")
                with c2:
                    st.write(f"{task.get('duration')}m")
                with c3:
                    if st.button("Done",key=f"btn_{task['id']}"):
                        requests.patch(f"{API_BASE_URL}/{task['id']}/complete")
                        st.rerun()
                st.divider()
    else:
        st.error("Backend Server is Offline. start the FastAPI server.")

    
#-------------------Add task--------------------------------
with st.sidebar:
    st.header("Quick Add")
    with st.form("new_task", clear_on_submit = True):
        new_title = st.text_input("Task Title", placeholder="Ex: Go for a walk.")
        with st.expander("More Details"):
            c_a, c_b = st.columns(2)
            new_cat = st.selectbox("Category", ["Home","Errand","Work"])
            new_dur = st.slider("Duration (m)", 5, 120,20)
            new_pri = st.selectbox("priority",["High","Medium","Low"],index=1)
        submit = st.form_submit_button("Add Task")
        
        if submit and new_title:
            payload = {
                "title": new_title,
                "category": new_cat,
                "duration": int(new_dur),
                "priority": new_pri,
                "location": location_label,
                "weather": current_weather,
                "completed": False,
                "sync_status": "synced" if is_connected else "pending"
                # created_at: will be handled by pydantic default factory.
            }
            requests.post(f"{API_BASE_URL}", json = payload)
            st.rerun()
