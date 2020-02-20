import gym
import torch
import torch.nn as nn
import numpy as np
from matplotlib import pyplot as plt


PATH = 'Model.pt'
PATH2 = 'Model2.pt'


class Net(nn.Module):
    def __init__(self, obs_size, hidden_size, n_actions):
        super(Net, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_actions)
        )

    def forward(self, x):
        return self.net(x)


if __name__ == '__main__':

    render = lambda: plt.imshow(env.render(mode='rgb_array'))
    env = gym.make('CartPole-v0')

    obs_size = env.observation_space.shape[0]
    n_actions = env.action_space.n
    net = Net(obs_size, 128, n_actions)
    net = torch.load(PATH)

    net.eval()
    sm = nn.Softmax(dim=1)

    obs = env.reset()
    iter = 0
    while True:
        render()
        obs_v = torch.FloatTensor([obs])
        act_probs_v = sm(net(obs_v))
        act_probs = act_probs_v.data.numpy()[0]
        action = np.random.choice(len(act_probs), p=act_probs)
        next_obs, _, is_done, _ = env.step(action)
        if is_done:
            print("huutis")
            break
        iter += 1
        print(iter)
        obs = next_obs
    render()
    env.close()