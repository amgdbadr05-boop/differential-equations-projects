# Differential Equations: Two Python Projects

This package contains two beginner-friendly, interactive Python projects:

1. **Projectile Motion with Air Resistance**
2. **Disease Spread Simulation (SIR Model)**

Both projects use numerical methods to solve ordinary differential equations (ODEs):
- Forward Euler method
- Fourth-order Runge-Kutta method (RK4)

Each project has a Streamlit interface. The interface runs locally in your web browser, while the calculations are performed by Python.

## 1. Requirements

- Python 3.10 or newer
- Internet connection for the first installation only
- A terminal (Command Prompt, PowerShell, macOS Terminal, or VS Code terminal)

Check your Python installation:

```bash
python --version
```

On some computers, use:

```bash
python3 --version
```

## 2. Install and run the Projectile Motion project

Open a terminal and move into the project folder:

```bash
cd projectile_motion
```

Create a virtual environment (recommended):

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the libraries:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

A browser tab should open automatically. If it does not, copy the local URL printed in the terminal (usually `http://localhost:8501`) into your browser.

## 3. Install and run the SIR Model project

Open a **new terminal** or stop the first application with `Ctrl+C`. Move into the SIR project folder:

```bash
cd sir_model
```

Create and activate a virtual environment as shown above, then install:

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python -m streamlit run app.py
```

If port 8501 is already in use, Streamlit will offer another local address, often `http://localhost:8502`.

## 4. Run without the web interface (optional)

Each project also includes a command-line example:

```bash
python simulation.py
```

This prints sample results in the terminal. The Streamlit interface is the recommended way to explore the models and graphs.

## 5. What is inside each project?

### projectile_motion/
- `app.py`: interactive Streamlit application
- `simulation.py`: differential-equation model and Euler/RK4 solvers
- `requirements.txt`: required Python libraries

### sir_model/
- `app.py`: interactive Streamlit application
- `simulation.py`: SIR differential-equation model and Euler/RK4 solvers
- `requirements.txt`: required Python libraries

## 6. Numerical model notes

### Projectile motion
The model assumes:
- A point-mass projectile.
- Constant gravitational acceleration.
- Still air with constant density.
- Quadratic drag, proportional to the square of speed.
- No wind, lift, spin, or change in air density with altitude.
- The projectile starts and lands at the same ground level.

The drag force magnitude is:

`F_d = 0.5 * rho * Cd * A * v^2`

The horizontal and vertical velocity equations are:

`dvx/dt = -(k/m) * v * vx`

`dvy/dt = -g - (k/m) * v * vy`

where `k = 0.5 * rho * Cd * A` and `v = sqrt(vx^2 + vy^2)`.

### SIR model
The model assumes a closed, well-mixed population with no births, deaths, or migration during the simulation:

`dS/dt = -beta * S * I / N`

`dI/dt = beta * S * I / N - gamma * I`

`dR/dt = gamma * I`

`N = S + I + R`

Here, beta is the transmission-rate parameter and gamma is the recovery-rate parameter. These are simplified teaching models, not real-time forecasts or medical advice.

## 7. Euler and RK4

Euler uses the slope at the start of each time step:

`y_(n+1) = y_n + h*f(t_n, y_n)`

RK4 uses four slope estimates in each time step and combines them to obtain a more accurate update. In general, RK4 is more accurate than Euler for the same sufficiently small step size, but numerical accuracy still depends on the model and chosen step size.

## 8. Troubleshooting

- **`python` is not recognized:** install Python from https://www.python.org/downloads/ and select the option to add Python to PATH on Windows. You may need to use `py` instead of `python`.
- **`streamlit` is not recognized:** use `python -m streamlit run app.py` after installing the requirements.
- **Module not found:** make sure the correct project folder is open and run `python -m pip install -r requirements.txt`.
- **Browser does not open:** copy the local URL displayed in the terminal.
- **Stop the app:** click the terminal and press `Ctrl+C`.

## 9. GitHub upload

Create a separate GitHub repository for each project. In the project folder, run:

```bash
git init
git add .
git commit -m "Add differential equations simulation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your own repository URL. Do not share passwords or access tokens.

## 10. Suggested learning order

1. Read the model notes above.
2. Run the app without changing any parameters.
3. Change one parameter at a time.
4. Compare Euler and RK4.
5. Explain what each graph and output means.
6. Only then prepare the final presentation.
# differential-equations-projects
