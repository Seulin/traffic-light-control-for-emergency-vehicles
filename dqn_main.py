import gym

import os
import sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
import numpy as np
from sumo_rl import SumoEnvironment
import traci

from stable_baselines3.dqn.dqn import DQN

from map_file import get_map, out_folder

try:
    tag = int(sys.argv[1])
except IndexError:
    tag = 4

net_file, rou_file = get_map(tag)

env = SumoEnvironment(net_file=net_file, 
                        single_agent=True,
                        route_file=rou_file, 
                        out_csv_name= out_folder(tag) + 'dqn', #'outputs/big-intersection/dqn',
                        use_gui=True,
                        num_seconds=5400,
                        yellow_time=4,
                        min_green=5,
                        max_green=60)

model = DQN(
    env=env,
    policy="MlpPolicy",
    learning_rate=1e-3,
    buffer_size=50000,
    exploration_fraction=0.05,
    exploration_final_eps=0.02
)
model.learn(total_timesteps=100000)
