from stable_baselines3 import PPO
from env import Puissance4Env

env = Puissance4Env()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)
model.save("puissance4_ppo")
