from gym.envs.registration import register

register(
    id='MultiCar-v0',
    entry_point='Car-RL.MultiCar:MultiCarEnv'
)