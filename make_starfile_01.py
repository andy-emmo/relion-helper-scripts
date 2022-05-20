import pickle
import numpy as np
import os

# the filename of the particle subset
fn1 = './02_vae256_stateA/ind_keep.20538_particles.pkl'
f = open(fn1, 'rb')
particles = pickle.load(f)
f.close()
#print(type(particles))
#print(particles)
# it's an ndarray, make it a list
particles = particles.tolist()
#print(particles)

# path to the original starfile
fn2 = './job309/particles.star'
# first line of the data_particles loop, line numbers are 1-offset
first_line = 59
first_line -= 1

f = open(fn2)
data = f.read()
f.close()
data = data.split('\n')
#print(data[57])
#print(data[58])
#print(data[59])
hdr = data[:first_line]
#print(hdr)
data = data[first_line:]
print(data[0])
print(data[-1])
# there are 383193 particles
print('total number of particles: ', len(data))  # this returns 383195, there'll be a blank line at the end, but what is the other element?


fn3 = './particles_subset.star'
f = open(fn3, 'w')
for h in hdr:
    f.write(h + '\n')

for n, d in enumerate(data):
    if not n % 10000:
        print(n)
    if len(d) < 10:
        print('short line: ', n, d)
    else:
        if n in particles:
            f.write(d + '\n')
f.close()

