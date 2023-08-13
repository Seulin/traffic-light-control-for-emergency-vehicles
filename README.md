# Traffic light control for emergency vehicles

## Objective
1. Controls the traffic light so that emergency vehicles can pass through the intersection quickly
2. Adjusts the traffic light to reduce traffic congestion

## Stacks
RL: [sumo-rl library from LucasAlegre](https://github.com/LucasAlegre/sumo-rl)

Simulation: [SUMO (Simulation of Urban MObility)](https://www.eclipse.org/sumo/)

## Model
  - Algorithm: Q-learning
  - Agent: Traffic light
  - Action: possible green phases
  - State: vector of size 26 including the information about location/speed of emergency vehicle and traffic congestion
  - Reward Model
      - WT: average waiting time of vehicles <br>
      - EVS: emergency vehicle's speed <br>
      - $\alpha$: Weight to prioritize emergency vehicles
      - $Reward = -WT + EVS*\alpha$

## Result
![road](https://raw.githubusercontent.com/Seulin/Seulin.github.io/main/assets/images/posts/road.gif)
    <br>
- 60% reduction in emergency vehicle travel time

    | Fixed traffic light | Trained traffic light |
    | -- | -- |
    | ![EV_travel](https://raw.githubusercontent.com/Seulin/Seulin.github.io/main/assets/images/posts/evt-fixed.png) | ![EV_travel2](https://raw.githubusercontent.com/Seulin/Seulin.github.io/main/assets/images/posts/evt-learned.png) |
    | Avg: 145.3s | Avg: 61.4s |

- 15% reduction in normal vehicle latency

    | Fixed traffic light | Trained traffic light |
    | -- | -- |
    | ![Watiting time](https://raw.githubusercontent.com/Seulin/Seulin.github.io/main/assets/images/posts/awt-7000-fixed.png) | ![Waiting time](https://raw.githubusercontent.com/Seulin/Seulin.github.io/main/assets/images/posts/awt-7000-learned.png) |
    | Avg: 1552.3s | Avg: 1331.2s |

## Key Files

### ql_main.py
```bash
python ql_maiin.py {sumo-gui off(0)/on(1)} {map_number}
``` 
Traffic light training code using Q learning.

### outputs/2x2
Training result stored here.

### map_file.py
Code that determines the map and route according to map_number.

### sumo-rl/sumo_rl/agents/ql_agent.py
Q learning agent is implemented here.

### sumo-rl/sumo_rl/environment/traffic_signal.py
Traffic light is implemented here. You can also modify reward model here.
