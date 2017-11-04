from __future__ import print_function
import time
import numpy as np
import sys
import gym
from PIL import Image
from realenv.core.render.profiler import Profiler
from realenv.envs.husky_env import HuskyCameraEnv
import pybullet as p


class RandomAgent(object):
    """The world's simplest agent"""
    def __init__(self, action_space, is_discrete = False):
        self.action_space = action_space
        self.is_discrete = is_discrete
        
    def act(self, observation, reward=None):
        if self.is_discrete:
            action = np.random.randint(self.action_space.n)
        else:
            action = np.zeros(self.action_space.shape[0])
            if (np.random.random() < 0.5):
                action[np.random.choice(action.shape[0], 1)] = np.random.randint(0, 2)
        return action

if __name__ == '__main__':
    env = HuskyCameraEnv(human=True, timestep=1.0/(4 * 22), frame_skip=4, enable_sensors=True, is_discrete = True)
    env.reset()
    agent = RandomAgent(env.action_space, is_discrete = True)
    ob = None

    while 1:
        frame = 0
        score = 0
        restart_delay = 0
        obs = env.reset()
        while True:
            time.sleep(0.03)
            a = agent.act(obs)
            with Profiler("Agent step function"):
                obs, r, done, meta = env.step(a)
            score += r
            frame += 1

            if not done and frame < 60: continue
            if restart_delay==0:
                print("score=%0.2f in %i frames" % (score, frame))
                restart_delay = 20 * 6  # 2 sec at 60 fps
            else:
                restart_delay -= 1
                if restart_delay==0: break