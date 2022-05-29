#%%
import argparse
import os
import sys
#import pandas as pd

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

sys.path.append('sumo-rl/')

# import traci
import sumo_rl
from sumo_rl.agents.ql_agent import QLAgent
from sumo_rl.exploration.epsilon_greedy import EpsilonGreedy

from map_file import get_map, out_folder
import time

if __name__ == '__main__':

    alpha = 0.1
    gamma = 0.99
    runs = 30

    try:
        tag = int(sys.argv[1])
    except IndexError:
        tag = 2

    net_file, rou_file = get_map(tag)

    env = sumo_rl.env(
                          net_file=net_file,
                          route_file=rou_file,
                          use_gui=False,
                          min_green=8,
                          delta_time=5,
                          num_seconds=80000)

    for run in range(1, runs+1):

        start = time.time()

        env.reset()

        traci = env.unwrapped.env.sumo

        initial_states = {ts: env.observe(ts) for ts in env.agents}
        ql_agents = {ts: QLAgent(starting_state=env.unwrapped.env.encode(initial_states[ts], ts),
                                 state_space=env.observation_space(ts),
                                 action_space=env.action_space(ts),
                                 alpha=alpha,
                                 gamma=gamma,
                                 exploration_strategy=EpsilonGreedy(initial_epsilon=0.05, min_epsilon=0.005, decay=1)) for ts in env.agents}
        infos = []

        for i, agent in enumerate(env.agent_iter()):
            ###
            if traci.vehicle.getIDCount() == 0 and i > 100:
                break

            if i % 1000 == 0:
                print("CURRENT LOOP", i, time.time()-start)
            ###

            s, r, done, info = env.last()
            if ql_agents[agent].action is not None:
                ql_agents[agent].learn(next_state=env.unwrapped.env.encode(s, agent), reward=r)

            action = ql_agents[agent].act() if not done else None
            env.step(action)

            ###
            if i % 5000 == 0:
                env.unwrapped.env.save_csv(out_folder(tag) + f'QL{i}_{time.localtime().tm_hour}_{time.localtime().tm_min}', run)
                print("EV Travel time", env.unwrapped.env.ev_travel_time)
            ###

        ###
        print('EV Travel time', env.unwrapped.env.ev_travel_time)
        env.unwrapped.env.save_csv(out_folder(tag) + f'QL_{time.localtime().tm_hour}_{time.localtime().tm_min}', run)
        ###

        env.close()

        print("Elapsed time: ", time.time()-start)

# %%
