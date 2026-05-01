import numpy as np

x_dim = 400
y_dim = 200


def go_right(self):
    '''gives a decaying velocity equal to right edge minus
    horizontal position/2'''
    self.a = np.zeros((self.N, 2))
    self.v = (x_dim/2 - self.r) * np.array([1,0])/20

    #so this doesn't return a value, but rather updates the r,v,a accordingly...
    #this is actually in fact robust as hell, so we're ok.

def attraction(self):
    '''modeled after theory of gravitation'''

    #now we are  going to vectorize EVERYTHING BABYYYYYYYY
    # self.r # ~ (s.N, 2)
    # 1) create a difference tensor
    differences = self.r[np.newaxis, : ,:] - self.r[:, np.newaxis, :] # (N, N, 2)

    # 2) create magnitudes tensor
    magnitudes = np.linalg.norm(differences, axis = 2) # (N, N)
    # mask out own distance
    np.fill_diagonal(magnitudes, np.inf)
    magnitudes = magnitudes[:,:,np.newaxis] # (N, N, 1)

    # 3) create unit differences tensor
    unit_diff = differences / magnitudes # (N, N, 2)

    # 4) create forces tensor
    forces = unit_diff * (1/magnitudes**2) # (N, N, 2)

    # 5) sum all forces together (we assume mass == 1 here)
    accel = np.sum(forces, axis = 1)/self.mass # (N, 2)

    self.a = accel


def radial(self):
    '''Boid-style flocking: alignment + cohesion + separation.
    Three radii control behavior: alignment matches neighbor velocities,
    cohesion pulls toward group center, separation prevents overcrowding.'''
    d_align    = 50   # radius for velocity matching
    d_cohesion = 60   # radius for grouping toward center of mass
    d_sep      = 15   # personal space radius
    w_align    = 0.06 # how strongly to match neighbor velocity
    w_cohesion = 0.003 # how strongly to move toward group center
    w_sep      = 0.8  # how strongly to push apart when too close
    max_speed  = 30.0

    # diff[i,j] = r[j] - r[i]  (vector pointing from i toward j)
    diff = self.r[np.newaxis, :, :] - self.r[:, np.newaxis, :]  # (N, N, 2)
    dist = np.linalg.norm(diff, axis=2)                          # (N, N)
    np.fill_diagonal(dist, np.inf)

    # --- Alignment: match average velocity of neighbors ---
    align_mask = (dist <= d_align).astype(float)                                         # (N, N)
    n_align    = np.maximum(align_mask.sum(axis=1, keepdims=True), 1)                    # (N, 1)
    avg_vel    = (align_mask[:, :, np.newaxis] * self.v[np.newaxis, :, :]).sum(axis=1) / n_align
    a_align    = w_align * (avg_vel - self.v)

    # --- Cohesion: steer toward center of mass of neighbors ---
    cohesion_mask = (dist <= d_cohesion).astype(float)
    n_cohesion    = np.maximum(cohesion_mask.sum(axis=1, keepdims=True), 1)
    center        = (cohesion_mask[:, :, np.newaxis] * self.r[np.newaxis, :, :]).sum(axis=1) / n_cohesion
    a_cohesion    = w_cohesion * (center - self.r)

    # --- Separation: push away from neighbors within personal space ---
    # -diff points from j back toward i (away from neighbor)
    safe_dist = np.where(dist < d_sep, np.maximum(dist, 0.1), np.inf)
    a_sep = w_sep * ((-diff) / (safe_dist[:, :, np.newaxis] ** 2)).sum(axis=1)

    self.a = a_align + a_cohesion + a_sep

    # --- Border repulsion ---
    b   = 50
    r_a = 3
    self.a[self.r[:, 0] >  x_dim - b, 0] -= r_a
    self.a[self.r[:, 0] < -x_dim + b, 0] += r_a
    self.a[self.r[:, 1] >  y_dim - b, 1] -= r_a
    self.a[self.r[:, 1] < -y_dim + b, 1] += r_a

    # --- Speed cap ---
    speed = np.linalg.norm(self.v, axis=1, keepdims=True)
    self.v = np.where(speed > max_speed, self.v / speed * max_speed, self.v)


'''this dictionary stores functions for movement based off of 
the argument given to school'''
mvmt_dict = {
    'radial' : radial,
    'attraction' : attraction,
    'go_right' : go_right #add a comma if you add more
}


class Flock:
    '''parent class for schools of fish'''

    #iterations gives us low long the history is going to be


    def __init__(self, N, iterations=1):

        self.N = N # Flock.N, this is number of fish.


        self.r = np.zeros((self.N, 2))
        self.v = np.zeros((self.N, 2))
        self.a = np.zeros((self.N, 2))
        self.iterations=iterations

        #3 dimensional tensor of the POSITION history. we will edit as we go.
        self.history = np.zeros((self.iterations, self.N, 2 ))

    #placeholder function for real acceleration calculations below
    def calc_accel(self):
        self.a = np.zeros((self.N, 2))
        #this will be overridden by the school definition of calc_accel

    def calc_vel(self):
        self.v = self.v + self.a
    
    def calc_pos(self):
        self.r = self.r + self.v

    def move_once(self):
        self.calc_accel()
        self.calc_vel()
        self.calc_pos()

    def full_calculation(self):
        i = 0
        while i < self.iterations:
            self.history[i] = self.r #record
            self.move_once() #update
            i+=1
        # print(self.history)
        return self.history
    
class School(Flock):
    '''here we may insert the type of movement'''

    def __init__(self, mvmt_type, N, iterations=1, mass=.01):
        super().__init__(N=N, iterations=iterations)
        self.mvmt = mvmt_dict[mvmt_type] #this is a function now
        self.mass = mass

    # override parent calculation of acceleration
    def calc_accel(self):
        #based off of mvmt type
        self.mvmt(self)    

    

