"""Classic SIR infectious-disease model.

State vector: [S, I, R]
Time unit must match the units used for beta and gamma.
"""
from __future__ import annotations
import numpy as np


def sir_derivatives(state, beta, gamma, population):
    """Return derivatives [dS/dt, dI/dt, dR/dt]."""
    susceptible, infected, recovered = state
    new_infections = beta * susceptible * infected / population
    new_recoveries = gamma * infected
    return np.array([
        -new_infections,
        new_infections - new_recoveries,
        new_recoveries,
    ], dtype=float)


def euler_step(function, state, dt, *args):
    return state + dt * function(state, *args)


def rk4_step(function, state, dt, *args):
    k1 = function(state, *args)
    k2 = function(state + 0.5 * dt * k1, *args)
    k3 = function(state + 0.5 * dt * k2, *args)
    k4 = function(state + dt * k3, *args)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def simulate_sir(population=10000, initial_infected=10, beta=0.3, gamma=0.1,
                 days=160, dt=0.1, method="RK4"):
    """Return time series for S, I, and R."""
    if population <= 0:
        raise ValueError("Population must be positive.")
    if not 0 <= initial_infected <= population:
        raise ValueError("Initial infected must be between zero and population.")
    if beta < 0 or gamma < 0 or days <= 0 or dt <= 0:
        raise ValueError("Rates must be non-negative; days and dt must be positive.")

    initial_state = np.array([
        population - initial_infected,
        initial_infected,
        0.0,
    ], dtype=float)

    stepper = rk4_step if method.upper() == "RK4" else euler_step
    args = (beta, gamma, float(population))

    count = int(np.ceil(days / dt))
    times = np.zeros(count + 1)
    states = np.zeros((count + 1, 3))
    states[0] = initial_state

    for index in range(count):
        actual_dt = min(dt, days - times[index])
        states[index + 1] = stepper(sir_derivatives, states[index], actual_dt, *args)
        # Small floating-point deviations can occur; clip and renormalize.
        states[index + 1] = np.maximum(states[index + 1], 0.0)
        total = states[index + 1].sum()
        if total > 0:
            states[index + 1] *= population / total
        times[index + 1] = times[index] + actual_dt

    susceptible, infected, recovered = states.T
    peak_index = int(np.argmax(infected))
    return {
        "time": times,
        "S": susceptible,
        "I": infected,
        "R": recovered,
        "peak_infected": float(infected[peak_index]),
        "peak_day": float(times[peak_index]),
        "final_recovered": float(recovered[-1]),
        "final_susceptible": float(susceptible[-1]),
    }


def main():
    result = simulate_sir()
    print("SIR Disease Spread Simulation (RK4)")
    print(f"Peak infected     : {result['peak_infected']:.0f} people")
    print(f"Peak infection day: {result['peak_day']:.1f} days")
    print(f"Recovered at end  : {result['final_recovered']:.0f} people")


if __name__ == "__main__":
    main()
