import matplotlib.pyplot as plt
from classes import Flock
from classes import School
from classes import mvmt_dict
import matplotlib.animation as anim
import numpy as np
import random 
from classes import x_dim, y_dim

iterations = 500

def main():

    # get random seed
    random.seed(42)



    s = School(N=100, iterations=iterations, mvmt_type='radial')
    #parameterize the bounds
    v = 10
    r = 100
    # 1) preset the positions of the N particles
    s.r = np.random.uniform(low=-r, high=r, size=(s.N, 2))
    # s.a is handled in initialization
    s.v = np.random.uniform(low=-v, high=v, size=(s.N, 2))


    history = s.full_calculation()
    fig = plt.figure(figsize=(12,6))
    
    #make size work with matrix minima/maxima
    x_max = np.max(np.abs(history[:,:,0]))
    y_max = np.max(np.abs(history[:,:,1]))

    ax = fig.add_subplot(111)
    # ax.set_xlim(-x_max, x_max)
    # ax.set_ylim(-y_max, y_max)
    ax.set_xlim(-x_dim, x_dim)
    ax.set_ylim(-y_dim, y_dim)

    scatter = ax.scatter(history[0,:,0], history[0,:,1], s=10, color='blue')


    animation = anim.FuncAnimation(
        func=update, 
        frames=iterations, #number of frames to animate
        fig=fig, 
        fargs=(history, scatter), 
        interval = 30 #number of milliseconds per frame
        )

    plt.show()

def update(frame:int, history, scatter):
    # 1. Grab the new coordinates
    current_positions = history[frame, :, :]
    
    # 2. Press the remote control to move the paint!
    scatter.set_offsets(current_positions)
    
    # 3. Return the updated scatter object (with a comma!)
    return scatter,

if __name__ == "__main__":

    main()