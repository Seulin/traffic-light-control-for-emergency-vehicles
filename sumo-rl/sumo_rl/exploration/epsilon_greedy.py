import numpy as np
from gym import spaces


class EpsilonGreedy:

    def __init__(self, initial_epsilon=1.0, min_epsilon=0.0, decay=0.99):
        self.initial_epsilon = initial_epsilon
        self.epsilon = initial_epsilon
        self.min_epsilon = min_epsilon
        self.decay = decay

    def choose(self, q_table, state, action_space):
        if np.random.rand() < self.epsilon:
            action = int(action_space.sample())
            # print("random ", action)
        else:
            ###
            # action = np.argmax(q_table[state])
            indices = np.argwhere(q_table[state] == np.max(q_table[state]))
            indices = indices.flatten().tolist()
            action = np.random.choice(indices, 1)[0]
            # if len(indices) < 3:
            #     print("Possible options :", len(indices))
            # print("choice ", action, "   possible ", indices)
            ###

        self.epsilon = max(self.epsilon*self.decay, self.min_epsilon)
        #print(self.epsilon)
        return action

    def reset(self):
        self.epsilon = self.initial_epsilon
