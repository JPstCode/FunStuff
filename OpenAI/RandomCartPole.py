import gym
from gym import wrappers
import matplotlib.pyplot as plt

if __name__ == '__main__':


    env = gym.make("CartPole-v0")
    render = lambda: plt.imshow(env.render(mode='rgb_array'))
    total_reward = 0.0
    total_steps = 0
    _,_,_,_ = env.reset()

    while True:
        render()
        action = env.action_space.sample()
        obs, reward, done, _ = env.step(action)

        total_reward += reward
        total_steps += 1
        if done:
            break

    render()
    print("Episode done in %d steps, total reward %.2f" % (total_steps, total_reward))

    env.close()