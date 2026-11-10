import matplotlib.pyplot as plt
import streamlit as st
from simulation import simulate_sir

st.set_page_config(page_title="SIR Disease Spread Simulator", page_icon="🦠", layout="wide")
st.title("Disease Spread Simulation: SIR Model")
st.write("Explore how susceptible, infected, and recovered populations change over time.")

with st.sidebar:
    st.header("Model parameters")
    population = st.number_input("Total population", min_value=100, max_value=10_000_000, value=10000, step=100)
    initial_infected = st.number_input("Initially infected people", min_value=1, max_value=int(population), value=min(10, int(population)), step=1)
    beta = st.slider("Transmission rate (β)", 0.01, 1.0, 0.30, 0.01)
    gamma = st.slider("Recovery rate (γ)", 0.01, 1.0, 0.10, 0.01)
    days = st.slider("Simulation duration (days)", 30, 365, 160, 5)
    dt = st.select_slider("Time step (days)", options=[0.01, 0.05, 0.1, 0.25, 0.5], value=0.1)
    method = st.selectbox("Numerical method", ["RK4", "Euler"])

result = simulate_sir(int(population), int(initial_infected), beta, gamma, days, dt, method)

c1, c2, c3 = st.columns(3)
c1.metric("Peak infected", f"{result['peak_infected']:,.0f} people")
c2.metric("Peak infection day", f"{result['peak_day']:.1f} days")
c3.metric("Recovered at end", f"{result['final_recovered']:,.0f} people")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(result["time"], result["S"], label="Susceptible (S)", linewidth=2)
ax.plot(result["time"], result["I"], label="Infected (I)", linewidth=2)
ax.plot(result["time"], result["R"], label="Recovered (R)", linewidth=2)
ax.set_xlabel("Time (days)")
ax.set_ylabel("Number of people")
ax.set_title(f"SIR population over time ({method})")
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)
plt.close(fig)

with st.expander("See the mathematical model"):
    st.latex(r"\frac{dS}{dt}=-\frac{\beta SI}{N}")
    st.latex(r"\frac{dI}{dt}=\frac{\beta SI}{N}-\gamma I")
    st.latex(r"\frac{dR}{dt}=\gamma I")
    st.write("N = S + I + R. The model assumes a closed, well-mixed population.")

st.subheader("Compare numerical methods")
euler = simulate_sir(int(population), int(initial_infected), beta, gamma, days, dt, "Euler")
rk4 = simulate_sir(int(population), int(initial_infected), beta, gamma, days, dt, "RK4")
st.dataframe({
    "Method": ["Euler", "RK4"],
    "Peak infected (people)": [euler["peak_infected"], rk4["peak_infected"]],
    "Peak day": [euler["peak_day"], rk4["peak_day"]],
    "Recovered at end": [euler["final_recovered"], rk4["final_recovered"]],
}, use_container_width=True)

st.caption("Educational mathematical model, not a real-world outbreak forecast or medical advice.")
