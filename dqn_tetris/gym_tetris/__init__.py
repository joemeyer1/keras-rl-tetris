from gym.envs.registration import register

register(
    id='tetris-v0',
    entry_point='gym_tetris.envs:TetrisEnv',
)
register(
    id='tetris-extrahard-v0',
    entry_point='gym_tetris.envs:TetrisExtraHardEnv',
)