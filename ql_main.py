import argparse
import os
import sys
import pandas as pd

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

# import traci
import sumo_rl
from sumo_rl.agents import QLAgent
from sumo_rl.exploration import EpsilonGreedy


from map_file import get_map, out_folder

if __name__ == '__main__':

    alpha = 0.1
    gamma = 0.99
    decay = 1
    runs = 1

    try:
        tag = int(sys.argv[1])
    except IndexError:
        tag = 21

    net_file, rou_file = get_map(tag)

    env = sumo_rl.env(
                          net_file=net_file,
                          route_file=rou_file,
                          use_gui=True,
                          min_green=8,
                          delta_time=5,
                          num_seconds=80000)

    for run in range(1, runs+1):
        env.reset()

        traci = env.unwrapped.env.sumo

        initial_states = {ts: env.observe(ts) for ts in env.agents}
        ql_agents = {ts: QLAgent(starting_state=env.unwrapped.env.encode(initial_states[ts], ts),
                                 state_space=env.observation_space(ts),
                                 action_space=env.action_space(ts),
                                 alpha=alpha,
                                 gamma=gamma,
                                 exploration_strategy=EpsilonGreedy(initial_epsilon=0.05, min_epsilon=0.005, decay=decay)) for ts in env.agents}
        infos = []
        for i, agent in enumerate(env.agent_iter(max_iter=10**9)):
            s, r, done, info = env.last()
            if ql_agents[agent].action is not None:
                ql_agents[agent].learn(next_state=env.unwrapped.env.encode(s, agent), reward=r)

            action = ql_agents[agent].act() if not done else None
            env.step(action)

        env.unwrapped.env.save_csv(out_folder(tag) + 'ql', run)
        env.close()