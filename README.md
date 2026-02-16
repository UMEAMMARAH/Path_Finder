# Path_Finder
Project Description

This project demonstrates the behavior of uninformed search algorithms in a dynamic grid environment using Python and Pygame. The primary goal is to visualize how algorithms “think” step by step, highlighting:

Nodes being explored (explored set)

Nodes waiting to be explored (frontier)

The final path found

Dynamic obstacles can appear randomly during the search, forcing the algorithm to adapt and re-plan its path.

Key Features:

Visual GUI for real-time step-by-step search

Dynamic obstacles (runtime events) with random probability

Highlighted frontier, explored nodes, and final path

Six algorithms implemented:

Breadth-First Search (BFS)

Depth-First Search (DFS)

Uniform-Cost Search (UCS)

Depth-Limited Search (DLS)

Iterative Deepening DFS (IDDFS)

Bidirectional Search

Start and Goal points visually marked

Configurable grid size, cell size, and search speed

Clear GUI title: “GOOD PERFORMANCE TIME APP”

Installation

Clone this repository:

git clone https://github.com/<your-username>/good-performance-time-app.git
cd good-performance-time-app


Install dependencies:

pip install pygame numpy


Run the application:

python main.py


Note: Make sure Python 3.x is installed on your system.

Usage

The application automatically runs all six search algorithms sequentially.

Watch the frontier (BLUE), explored nodes (PURPLE), and final path (YELLOW).

Dynamic obstacles appear randomly (GRAY) as the search progresses.

The GUI updates step by step to visualize the algorithm’s decision-making process.

After completion, a final message is displayed: "GOOD PERFORMANCE TIME APP — All algorithms finished."
