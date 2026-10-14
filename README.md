# OS Deadlock Detection & Safety Simulator

An interactive, graphical desktop application built with Python and Tkinter to simulate, analyze, and visualize Operating System deadlock detection and safety state verification using the **Banker's Algorithm**.

This project allows students, developers, and OS enthusiasts to inspect how allocation matrices, maximum demand vectors, and system availability affect process safety and resource management in real time.

---

## 🌟 Key Features

* **Interactive Matrix Configuration**: Modify the **Allocation Matrix**, **Max Demand Matrix**, and **Available Resources Vector** directly via a user-friendly GUI grid.


* **Banker's Algorithm Safety Engine**: Automatically computes the dynamic **Need Matrix** ($Need = Max - Allocation$) and checks if the system resides in a safe state.


* **Safe Sequence Generation**: Traces process execution step-by-step and displays a valid safe execution sequence (e.g., `P1 -> P3 -> P4 -> P0 -> P2`) upon success.


* **Deadlock Detection & Visual Alerting**: Identifies locked processes during resource starvation and visually highlights problem process rows in red within the UI.


* **Simulation Trace Terminal**: Integrated real-time console log tracking internal variable changes, such as the dynamic system work vector updates.


* **Random Vector Injector**: Generates randomized, valid matrix configurations with one click for fast scenario testing.


* **Force Deadlock Attack Simulator**: Instantly applies severe resource constraints and high process demands to demonstrate system failure states.



---

## 💡 Practical Applications

1. **Operating Systems Education**: Serves as a visual aid for computer science students and instructors studying process synchronization, resource allocation, and deadlock avoidance/prevention strategies.


2. **Algorithm Verification**: Demonstrates how the Banker's Algorithm prevents circular wait and resource starvation in multi-threaded or multi-process environments.


3. **Interactive Testing & Debugging**: Provides a playground to evaluate safe vs. unsafe states under varying resource availability and allocation thresholds without writing code for each test case.



---

## 🛠️ Project Architecture & Tech Stack

* **Language**: Python 3.x


* **GUI Framework**: Tkinter (Standard Python Library)


* **Core Algorithm**: Banker's Safety Algorithm


* **Supported Scope**: 5 Processes ($P_0$ to $P_4$) across 3 Resource Types ($R_0$, $R_1$, $R_2$)



---

## 🚀 Getting Started

### Prerequisites

* **Python 3.6+** installed on your system.


* Tkinter is included by default in standard Python installations on Windows and macOS. Linux users may need to install it via their package manager (e.g., `sudo apt install python3-tk`).

### Installation & Execution

1. **Clone the repository** (or download `main.py`):
```bash
git clone https://github.com/your-username/os-deadlock-simulator.git
cd os-deadlock-simulator

```


2. **Run the simulator**:
```bash
python main.py

```



---

## 🖥️ Usage Guide

1. **Check Deadlock State**: Click **"Check Deadlock State"** to run the safety algorithm on the current matrix inputs.


2. **Inject Random Vectors**: Click **"Inject Random Vectors"** to generate new random allocation values and available resource amounts.


3. **Force Attack Deadlock**: Click **"Force Attack Deadlock"** to simulate an unsafe state where allocation demands exceed available system resources.


4. **Inspect Terminal Log**: Review the dark console log on the right panel to trace step-by-step allocations and updates to the working vector.
