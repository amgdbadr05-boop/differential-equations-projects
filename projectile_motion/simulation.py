"""Projectile motion with quadratic air resistance.

State vector: [x, y, vx, vy]
Units: SI (m, s, kg).
"""
from __future__ import annotations
import math
import numpy as np


def derivatives(state, mass, rho, drag_coefficient, area, gravity=9.81, air_resistance=True):
    """Return derivatives [dx/dt, dy/dt, dvx/dt, dvy/dt]."""
    x, y, vx, vy = state
    speed = math.hypot(vx, vy)

    if air_resistance:
        k_over_m = 0.5 * rho * drag_coefficient * area / mass
        ax = -k_over_m * speed * vx
        ay = -gravity - k_over_m * speed * vy
    else:
        ax = 0.0
        ay = -gravity

    return np.array([vx, vy, ax, ay], dtype=float)


def euler_step(function, state, dt, *args):
    return state + dt * function(state, *args)


def rk4_step(function, state, dt, *args):
    k1 = function(state, *args)
    k2 = function(state + 0.5 * dt * k1, *args)
    k3 = function(state + 0.5 * dt * k2, *args)
    k4 = function(state + dt * k3, *args)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def simulate_projectile(
    speed=25.0,
    angle_degrees=45.0,
    mass=0.145,
    rho=1.225,
    drag_coefficient=0.47,
    area=0.0042,
    dt=0.01,
    method="RK4",
    air_resistance=True,
    gravity=9.81,
    max_time=30.0,
):
    """Simulate until the projectile returns to ground level."""
    if mass <= 0 or dt <= 0 or area < 0 or rho < 0 or drag_coefficient < 0:
        raise ValueError("Mass and time step must be positive; drag parameters cannot be negative.")

    angle = math.radians(angle_degrees)
    initial_state = np.array([
        0.0,
        0.0,
        speed * math.cos(angle),
        speed * math.sin(angle),
    ], dtype=float)

    stepper = rk4_step if method.upper() == "RK4" else euler_step
    args = (mass, rho, drag_coefficient, area, gravity, air_resistance)

    times = [0.0]
    states = [initial_state.copy()]
    state = initial_state.copy()
    time = 0.0

    while time < max_time:
        previous = state.copy()
        next_state = stepper(derivatives, state, dt, *args)
        next_time = time + dt

        # Stop at the first descending crossing of ground level.
        if next_state[1] < 0 and next_state[3] < 0 and next_time > 0:
            fraction = previous[1] / (previous[1] - next_state[1]) if previous[1] != next_state[1] else 0.0
            fraction = min(max(fraction, 0.0), 1.0)
            impact_state = previous + fraction * (next_state - previous)
            times.append(time + fraction * dt)
            states.append(impact_state)
            break

        times.append(next_time)
        states.append(next_state.copy())
        state = next_state
        time = next_time

    data = np.asarray(states)
    t = np.asarray(times)
    x, y, vx, vy = data.T
    return {
        "time": t,
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "range": float(x[-1]),
        "flight_time": float(t[-1]),
        "max_height": float(np.max(y)),
        "impact_speed": float(math.hypot(vx[-1], vy[-1])),
    }


def main():
    result = simulate_projectile()
    print("Projectile Motion with Air Resistance (RK4)")
    print(f"Horizontal range : {result['range']:.3f} m")
    print(f"Maximum height   : {result['max_height']:.3f} m")
    print(f"Flight time      : {result['flight_time']:.3f} s")
    print(f"Impact speed     : {result['impact_speed']:.3f} m/s")


if __name__ == "__main__":
    main()
