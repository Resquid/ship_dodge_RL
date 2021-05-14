from gym.envs.registration import register
import gym
env_dict = gym.envs.registration.registry.env_specs.copy()
for env in env_dict:
    if "Pygame-v0" in env:
         print("Remove {} from registry".format(env))
         del gym.envs.registration.registry.env_specs[env]

register(
    id='Pygame-v0',
    entry_point='gym_game.envs:CustomEnv',
    max_episode_steps=2000,
)