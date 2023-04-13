# Traffic light control for emergency vehicles

###
[use sumo-rl library from LucasAlegre](https://github.com/LucasAlegre/sumo-rl)

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
