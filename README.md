# 🚗 Differential-Drive-Robot-Simulation-with-A-Pathfinding

This project simulates a **differential drive robot** navigating a 2D grid world using the **A\* (A-star) pathfinding algorithm** to plan a path around obstacles. The simulation is implemented using **Pygame** and allows for both autonomous and manual control of the robot.

---

## 🧠 Features

- ✅ Differential drive kinematics simulation
- ✅ A\* pathfinding to find shortest path to the goal
- ✅ Obstacle avoidance during planning
- ✅ Real-time simulation and rendering using `pygame`
- ✅ Manual keyboard control:
  - `↑` Move Forward
  - `↓` Move Backward
  - `←` Turn Left
  - `→` Turn Right
- ✅ Visual indicators:
  - Red line = Robot path (actual trajectory)
  - Yellow line = Planned path from A*
  - Gray blocks = Obstacles
  - Green circle = Goal location

---

## 📸 Screenshot

*(Add a screenshot of the simulation here)*

---

## 📂 Files

- `main.py` – Main simulation script
- `car.png` – Image file used to represent the robot

---

## 📦 Requirements

- Python 3.x
- pygame

### 🛠 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/differential-drive-robot-sim.git
   cd differential-drive-robot-sim
