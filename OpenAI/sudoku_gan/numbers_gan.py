import random
import argparse
import cv2 as cv

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter

import torchvision.utils as vutils
import torchvision.transforms as tvtrans

from matplotlib import pyplot as plt

import gym.spaces


import numpy as np

log = gym.logger
log.set_level(gym.logger.INFO)

LATENT_VECTOR_SIZE = 100
DISCR_FILTERS = 45
GENER_FILTERS = 45
BATCH_SIZE = 16

# dimension input image will be rescaled
IMAGE_SIZE = 45

LEARNING_RATE = 0.0001
REPORT_EVERY_ITER = 10
SAVE_IMAGE_EVERY_ITER = 10


# Wrapper around the GYM game
# class InputWrapper(gym.ObservationWrapper):
#     def __init__(self, *args):
#         super(InputWrapper, self).__init__(*args)
#         assert isinstance(self.observation_space, gym.spaces.Box)
#         old_space = self.observation_space
#         self.observation_space = gym.spaces.Box(self.observation(old_space.low),
#                                                 self.observation(old_space.high), dtype=np.float32)
#
#     def observation(self, observation):
#
#         # Resize image
#         new_obs = cv.resize(observation, (IMAGE_SIZE, IMAGE_SIZE))
#         # Transform (210,160,3) -> (3,210,160)
#         new_obs = np.moveaxis(new_obs,2,0)
#         return new_obs.astype(np.float32)/ 255.0

class Discriminator(nn.Module):
    def __init__(self, input_shape):
        super(Discriminator, self).__init__()
        # Pipeline for converting image to single number
        self.conv_pipe = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=DISCR_FILTERS, kernel_size=4, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=DISCR_FILTERS, out_channels=DISCR_FILTERS*2, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(DISCR_FILTERS*2),
            nn.ReLU(),
            nn.Conv2d(in_channels=DISCR_FILTERS*2, out_channels=DISCR_FILTERS*4, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(DISCR_FILTERS * 4),
            nn.ReLU(),
            nn.Conv2d(in_channels=DISCR_FILTERS*4, out_channels=DISCR_FILTERS*8, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(DISCR_FILTERS*8),
            nn.ReLU(),
            nn.Conv2d(in_channels=DISCR_FILTERS*8, out_channels=1, kernel_size=2, stride=1, padding=0),
            nn.Sigmoid()
        )

    def forward(self, x):
        conv_out = self.conv_pipe(x)
        return conv_out.view(-1,1).squeeze(dim=1)

class Generator(nn.Module):
    def __init__(self, output_shape):
        super(Generator, self).__init__()
        # pipe deconvolves input vector into (1, 45, 45) image
        self.pipe = nn.Sequential(
            # in = 1x1, out = 4x4
            nn.ConvTranspose2d(in_channels=LATENT_VECTOR_SIZE, out_channels=GENER_FILTERS * 5,
                               kernel_size=4, stride=1, padding=0),
            nn.BatchNorm2d(GENER_FILTERS * 5),
            nn.ReLU(),
            # in = 4x4, out = 8x8
            nn.ConvTranspose2d(in_channels=GENER_FILTERS * 5, out_channels=GENER_FILTERS * 3,
                               kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(GENER_FILTERS * 3),
            nn.ReLU(),
            # in = 8x8, out = 16x16
            nn.ConvTranspose2d(in_channels=GENER_FILTERS * 3, out_channels=GENER_FILTERS * 3,
                               kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(GENER_FILTERS * 3),
            nn.ReLU(),
            # in = 16x16, out = 32x32
            nn.ConvTranspose2d(in_channels=GENER_FILTERS * 3, out_channels=GENER_FILTERS,
                               kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(GENER_FILTERS),
            nn.ReLU(),

            # Final dimension = stride*(n - 1) + kernel - 2*padding
            # 45 = 1*(32-1) + 14 - 2*0
            nn.ConvTranspose2d(in_channels=GENER_FILTERS, out_channels=output_shape[0],
                               kernel_size=14, stride=1, padding=0),
            nn.Tanh()
        )
    def forward(self, x):
        return self.pipe(x)

# # Sample infinitely the environment from the provided array
# def iterate_batches(, batch_size=BATCH_SIZE):
#
#     batch = [e.reset() for e in envs]
#     env_gen = iter(lambda: random.choice(envs), None)
#
#     while True:
#         e = next(env_gen)
#         obs, reward, is_done, _  = e.step(e.action_space.sample())
#         if np.mean(obs) > 0.01:
#             batch.append(obs)
#         if len(batch) == batch_size:
#             yield torch.FloatTensor(batch)
#             batch.clear()
#         if is_done:
#             e.reset()

if __name__ == '__main__':

    # Use to enable GPU/CPU computation mode
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuda", default=False, action='store_true')
    args = parser.parse_args()

    #device = torch.device("cuda" if args.cuda else "cpu")
    device = torch.device('cpu')

    images = np.load('images.npy')
    labels = np.load('labels.npy')

    #input_shape_dis = (1,45,45)
    input_shape = (1, 45, 45)

    # Create objects: a summary writer, both networks, a loss function and two optimizers
    writer = SummaryWriter()
    net_discr = Discriminator(input_shape=input_shape).to(device)
    net_gener = Generator(output_shape=input_shape).to(device)

    objective = nn.BCELoss()
    gen_optimizer = optim.Adam(params=net_gener.parameters(), lr=LEARNING_RATE)
    dis_optimizer = optim.Adam(params=net_discr.parameters(), lr=LEARNING_RATE)

    gen_losses = []
    dis_losses = []
    iter_no = 0

    true_labels_v = torch.ones(BATCH_SIZE, dtype=torch.float32, device=device)
    fake_labels_v = torch.zeros(BATCH_SIZE, dtype=torch.float32, device=device)

    for i in range(0, len(images), BATCH_SIZE):

        batch_v = torch.FloatTensor([images[i:i+BATCH_SIZE]]).reshape([-1,1,45,45])
        #batch_visualization = [images[i:i+BATCH_SIZE]]

        # Generate extra fake samples, input is in 4D: batch, filters, x, y
        gen_inpput_v = torch.FloatTensor(BATCH_SIZE, LATENT_VECTOR_SIZE, 1,1).normal_(1,0).to(device)
        gen_output_v = net_gener(gen_inpput_v)
        batch_v = batch_v.to(device)

        dis_optimizer.zero_grad()
        dis_output_true_v = net_discr(batch_v)
        dis_output_fake_v = net_discr(gen_output_v.detach())
        dis_loss = objective(dis_output_true_v, true_labels_v) + objective(dis_output_fake_v, fake_labels_v)
        dis_loss.backward()
        dis_optimizer.step()
        dis_losses.append(dis_loss.item())

        gen_optimizer.zero_grad()
        dis_output_v = net_discr(gen_output_v)
        gen_loss_v = objective(dis_output_v, true_labels_v)
        gen_loss_v.backward()
        gen_optimizer.step()
        gen_losses.append(gen_loss_v.item())

        iter_no += 1
        if iter_no % REPORT_EVERY_ITER == 0:
            log.info("Iter %d: gen_loss=%.3e, dis_loss=%.3e",iter_no, np.mean(gen_losses), np.mean(dis_losses))
            writer.add_scalar("gen_loss", np.mean(gen_losses), iter_no)
            writer.add_scalar("dis_loss", np.mean(dis_losses), iter_no)
            gen_losses = []
            dis_losses = []
        if iter_no % SAVE_IMAGE_EVERY_ITER == 0:
            writer.add_image("fake", vutils.make_grid(gen_output_v.data[:45]), iter_no)
            writer.add_image("real", vutils.make_grid(batch_v.data[:45], nrow=8, normalize=True), iter_no)