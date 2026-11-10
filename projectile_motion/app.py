import matplotlib.pyplot as plt
import streamlit as st
from simulation import simulate_projectile

st.set_page_config(page_title="Projectile Motion Simulator", page_icon="🚀", layout="wide")
st.title("Projectile Motion with Air Resistance")
st.write("Explore how gravity and quadratic air resistance affect a launched object.")

with st.sidebar:
    st.header("Simulation parameters")
    speed = st.slider("Initial speed (m/s)", 5.0, 60.0, 25.0, 1.0)
    angle = st.slider("Launch angle (degrees)", 5, 85, 45, 1)
    mass = st.slider("Object mass (kg)", 0.05, 5.0, 0.145, 0.005)
    rho = st.slider("Air density (kg/m³)", 0.5, 1.5, 1.225, 0.025)
    cd = st.slider("Drag coefficient", 0.1, 1.5, 0.47, 0.01)
    area = st.slider("Cross-sectional area (m²)", 0.0005, 0.05, 0.0042, 0.0005)
    dt = st.select_slider("Time step (seconds)", options=[0.001, 0.005, 0.01, 0.02, 0.05], value=0.01)
    method = st.selectbox("Numerical method", ["RK4", "Euler"])

with_drag = simulate_projectile(speed, angle, mass, rho, cd, area, dt, method, True)
without_drag = simulate_projectile(speed, angle, mass, rho, cd, area, dt, method, False)

c1, c2, c3 = st.columns(3)
c1.metric("Range with drag", f"{with_drag['range']:.2f} m")
c2.metric("Maximum height", f"{with_drag['max_height']:.2f} m")
c3.metric("Flight time", f"{with_drag['flight_time']:.2f} s")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(with_drag["x"], with_drag["y"], label=f"With air resistance ({method})", linewidth=2)
ax.plot(without_drag["x"], without_drag["y"], "--", label="Without air resistance", linewidth=2)
ax.set_xlabel("Horizontal distance, x (m)")
ax.set_ylabel("Vertical height, y (m)")
ax.set_title("Projectile trajectories")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)
plt.close(fig)

with st.expander("See the mathematical model"):
    st.latex(r"\frac{dx}{dt}=v_x,\qquad \frac{dy}{dt}=v_y")
    st.latex(r"\frac{dv_x}{dt}=-\frac{k}{m}vv_x")
    st.latex(r"\frac{dv_y}{dt}=-g-\frac{k}{m}vv_y")
    st.latex(r"k=\frac{1}{2}\rho C_d A,\qquad v=\sqrt{v_x^2+v_y^2}")
    st.write("The model assumes constant air density, no wind, no lift, and a point-mass projectile.")

st.subheader("Compare numerical methods")
euler = simulate_projectile(speed, angle, mass, rho, cd, area, dt, "Euler", True)
rk4 = simulate_projectile(speed, angle, mass, rho, cd, area, dt, "RK4", True)
st.dataframe({
    "Method": ["Euler", "RK4"],
    "Range (m)": [euler["range"], rk4["range"]],
    "Maximum height (m)": [euler["max_height"], rk4["max_height"]],
    "Flight time (s)": [euler["flight_time"], rk4["flight_time"]],
}, use_container_width=True)

st.caption("Educational simulation. Results depend on the simplified assumptions and chosen time step.")
