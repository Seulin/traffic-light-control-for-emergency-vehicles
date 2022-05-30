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

def write(array):
    f = open("travel_time.txt", "a")
    for i in array:
        f.write(str(i)+", ")
    f.write("\n")
    f.close()

if __name__ == '__main__':

    alpha = 0.1
    gamma = 0.99
    runs = 1

    try:
        tag = int(sys.argv[2])
    except IndexError:
        tag = 2
    try:
        gui = int(sys.argv[1])
    except IndexError:
        gui = 0 # False

    net_file, rou_file = get_map(tag)

    env = sumo_rl.env(
                          net_file=net_file,
                          route_file=rou_file,
                          use_gui=gui,
                          min_green=8,
                          delta_time=5,
                          num_seconds=500000)

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
                print("SIM STEP ", env.unwrapped.env.sim_step)
            ###

            s, r, done, info = env.last()
            if ql_agents[agent].action is not None:
                ql_agents[agent].learn(next_state=env.unwrapped.env.encode(s, agent), reward=r)
            

            action = ql_agents[agent].act() if not done else None
            env.step(action)

            ###
            if i % 100000 == 0 and i > 0:
                # print("QTAB:E", ql_agents[agent].q_table)
                env.unwrapped.env.save_csv(out_folder(tag) + f'QL_{time.localtime().tm_hour}_{time.localtime().tm_min}', run)
                env.unwrapped.env.save_travel_time(out_folder(tag))
            ###

        ###
        env.unwrapped.env.save_travel_time(out_folder(tag))
        env.unwrapped.env.save_csv(out_folder(tag) + f'QL_{time.localtime().tm_hour}_{time.localtime().tm_min}', run)
        ###

        env.close()

        print("End of run, Elapsed time: ", time.time()-start)

# %%
