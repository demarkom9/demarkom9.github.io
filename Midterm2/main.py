import streamlit as st
import random
from Vehicles import Vehicle, GroundVehicle, Drone, UGV

# =========================
# Initialize Fleet (Session)
# =========================
if "fleet" not in st.session_state:
    st.session_state.fleet = {}

def add_vehicle(v):
    st.session_state.fleet[v.id] = v

def get_vehicle(vid):
    return st.session_state.fleet.get(vid)

def all_vehicles():
    return list(st.session_state.fleet.values())

# =========================
# UI
# =========================
st.title("🚚 Smart Fleet Management System")

# --- Add Vehicle ---
st.header("Add Vehicle")

col1, col2, col3 = st.columns(3)

with col1:
    vid = st.text_input("ID")
    name = st.text_input("Name")

with col2:
    vtype = st.selectbox("Type", ["Ground", "Drone", "UGV"])
    speed = st.number_input("Speed", 0, 200, 50)

with col3:
    if vtype == "Ground":
        extra_label = "Terrain (0=road, 1=offroad)"
    elif vtype == "Drone":
        extra_label = "Altitude (m)"
    else:
        extra_label = "Capacity (kg)"

    extra = st.number_input(extra_label, 0, 200, 50)

if st.button("Add Vehicle"):
    if not vid or not name:
        st.error("Please provide both ID and Name of Vehicle!!")

    elif vid in st.session_state.fleet:
        st.error(f"Vehicle ID {vid} already exists!")

    else:
        if vtype == "Ground":
            v = GroundVehicle(vid, name, speed, extra)
        elif vtype == "Drone":
            v = Drone(vid, name, speed, extra)
        else:
            v = UGV(vid, name, speed, extra)

        add_vehicle(v)
        st.success(f"Vehicle {name} added!")

# --- Display Fleet ---
st.header("Fleet Status")

if all_vehicles():
    for v in all_vehicles():
        battery = v.battery
        bar_color = "🟢" if battery > 60 else "🟡" if battery > 20 else "🔴"
        st.write(f"{bar_color} {v.info()}")
else:
    st.info("No vehicles in fleet yet.")

# --- Actions ---
st.header("Control Panel")

if all_vehicles():
    selected_id = st.selectbox("Select Vehicle", [v.id for v in all_vehicles()])
    vehicle = get_vehicle(selected_id)

    if vehicle:
        st.caption(
            f"Selected: **{vehicle.name}** | "
            f"Type: '{type(vehicle).__name__}' | "
            f"Battery: {vehicle.battery}%"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🛣️ Move"):
            msg = vehicle.move(random.randint(5, 15))
            st.info(msg)

    with col2:
        if st.button("🔋 Charge"):
            msg = vehicle.charge(random.randint(10, 30))
            st.info(msg)

    with col3:
        if st.button("📦 Deliver (UGV)"):
            if isinstance(vehicle, UGV):
                msg = vehicle.deliver(random.randint(1, 10))
                st.info(msg)
            else:
                st.error("Only UGV can deliver!")

else:
    st.warning("No vehicles in fleet yet.")