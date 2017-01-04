#!/usr/bin/env python
import sys
from beliefspace import *
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def scale_quadratic (x,y):
    return (x - 10.)

if __name__ == '__main__':

    # initial state
    x0 = np.array ([5., -5.])
    P0 = 3.**2.*np.eye (2)

    # final state
    #xf = np.array ([5., 5.])
    xf = np.array ([5., -3.])

    # initial control
    nsteps = 10
    u0 = np.tile ((1./DELTAT)*((xf-x0)/(nsteps-1)).reshape (2,1), (1, nsteps-1))

    ilqg = Belief_ilqg (x0, P0, u0, xf, scale_quadratic)
    x,P = ilqg.nominal_belief ()
    x_initial = x.copy ()

    # value iteration
    for i in range (5):
        ilqg.value_iteration ()

        #x,P = ilqg.nominal_belief ()
        #for Pi in P:
        #    print Pi
        #raw_input ('next...')

    x,P = ilqg.nominal_belief ()
    print(ilqg.ubar)

    fig_xy = plt.figure ()
    ax_xy = fig_xy.add_subplot (111)

    ax_xy.plot (x0[0], x0[1], 'g*', ms=15, mec='g', mew=3)
    ax_xy.plot (xf[0], xf[1], 'r+', ms=15, mew=5)
    ax_xy.plot (x[:,0], x[:,1], 'k.-', lw=2)
    ax_xy.axis ('equal')
    ax_xy.grid ()

    for ell_count in range(0, len(P)-1):
        cov = P[ell_count,:]
        
        lambda_, v = np.linalg.eig(cov)
        lambda_ = np.sqrt(lambda_)        
        try:
            ell = Ellipse(xy=(x[ell_count,0], x[ell_count,1]),
                  width=lambda_[0]*1*2, height=lambda_[1]*1*2,
                  angle=np.rad2deg(np.arccos(v[0, 0])))
            ell.set_facecolor('none')
        except(IndexError):
            print("Out of range")                
        
        ax_xy.add_artist(ell)

    # evaluate measurement model
    #axis = ax_xy.axis ()
    #X,Y = np.meshgrid (np.linspace (axis[0],axis[1]), 
    #        np.linspace (axis[2], axis[3]))
    #X,Y = np.meshgrid (np.linspace (0., 7.), np.linspace (-7., 0.))
    #Z = scale_quadratic (X,Y)
    #ax_xy.contourf (X, Y, Z, cmap=plt.cm.gray_r, 
    #        levels=np.linspace (Z.min (), Z.max (), 25))

    plt.show ()
    sys.exit (0)
