from stable_baselines3 import PPO
from env import Puissance4Env

model = PPO.load("puissance4_ppo")
env = Puissance4Env()
obs = env.reset()

<<<<<<< HEAD
=======

>>>>>>> origin/main
done = False
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, info = env.step(action)
    print(env.board)
