
import math
import scipy
import matplotlib.pyplot as plt
import numpy as np

## constants

c = 340 ## m/s, lambda = 0.17m
theta_s = math.pi/2 ## rad
freq = 2000 #kHz
N = [4, 8, 16, 50] ##  number of mics
d = 0.04 ## cm

figure_counter = 0


radians = list(np.linspace(0, math.pi, 1000))

## ---------------------------------------------------------------------------------------------------------------------

## TASK 1)

delay_sum_beam = []
for number in N:
    temporary = []
    for theta in radians:
        cons = (1 / number) * math.sin((number / 2) * 2 * math.pi * freq / c * d * (math.cos(theta) - math.cos(theta_s)))
        cons = cons/(math.sin((1/2) * 2*math.pi*freq/c * d*(math.cos(theta) - math.cos(theta_s))))
        temporary.append(cons)
    delay_sum_beam.append(temporary)


for i in range(len(N)):
    figure_counter += 1
    plt.figure(figure_counter)
    fig = plt.figure(figure_counter)
    ax = fig.add_subplot(111)
    ax.set_yscale('log')
    plt.plot(radians, abs(np.array(delay_sum_beam[i])))
    plt.title("DSB with " + str(N[i]) + " microphones, constant f, d and θ = pi/2")
    # plt.title("delay_sum_beam with " + str(N[i]) + " microphones")
    plt.xlabel("rad")
    plt.ylabel("delay_sum_beam amplitude")
    plt.savefig("Figures/1/delay_sum_beam[" + str(i) + "].png")

## PARATHROUME OTI OSO EUJANETAI TO N AUJANETAI H AKRIBEIA WS PROS TO THETA, DLD ANIXNEUOUME KALUTERA TO SHMA STH GWNIA THETA_S, STENOTEROS LOBOS
## MIKROTERA PLATH MAKRIA APO TO THETA_S

## ---------------------------------------------------------------------------------------------------------------------

## TASK 2)

distance = [0.04, 0.08, 0.16]

delay_sum_beam = []
for dist in distance:
    temporary = []
    for theta in radians:
        cons = (1 / N[1]) * math.sin((N[1] / 2) * 2 * math.pi * freq / c * dist * (math.cos(theta) - math.cos(theta_s)))
        cons = cons/(math.sin((1/2) * 2*math.pi*freq/c * dist*(math.cos(theta) - math.cos(theta_s))))
        temporary.append(cons)
    delay_sum_beam.append(temporary)


for i in range(len(distance)):
    figure_counter += 1
    fig = plt.figure(figure_counter)
    ax = fig.add_subplot(111)
    ax.set_yscale('log')
    plt.plot(radians, abs(np.array(delay_sum_beam[i])))
    plt.title("DSB with " + str(distance[i]) + " m distance")
    plt.xlabel("rad")
    plt.ylabel("delay_sum_beam amplitude")
    plt.savefig("Figures/1/2_delay_sum_beam[" + str(i) + "].png")


## GIA D = 0.16 PARABIAZETAI TO XWRIKO THEWRHMA DEIGMATOLIPSIAS GIA AUTO EXOUME 2 LOBOUS DEJIA KAI ARISTERA

## ---------------------------------------------------------------------------------------------------------------------

## TASK 3)

d = distance[1]
N = N[1]

radians = [0, math.pi/4, math.pi/3]
freqs = list(np.linspace(1, 8000, 16000))

delay_sum_beam = []
for rads in radians:
    temporary = []
    for freq in freqs:
        cons = (1 / N) * math.sin((N / 2) * 2 * math.pi * freq / c * d * (math.cos(rads) - math.cos(theta_s)))
        cons = cons/(math.sin((1/2) * 2*math.pi*freq/c * d*(math.cos(rads) - math.cos(theta_s))))
        temporary.append(cons)
    delay_sum_beam.append(temporary)

for i in range(len(radians)):
    figure_counter += 1
    fig = plt.figure(figure_counter)
    ax = fig.add_subplot(111)
    ax.set_yscale('log')
    plt.plot(freqs, abs(np.array(delay_sum_beam[i])))
    plt.title("DSB with m distance")
    plt.xlabel("rad")
    plt.ylabel("delay_sum_beam amplitude")
    plt.savefig("Figures/1/3_delay_sum_beam[" + str(i) + "].png")

plt.show()