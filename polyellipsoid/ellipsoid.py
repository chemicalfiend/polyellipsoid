from mbuild import Compound
from mbuild.lib.recipes import Polymer
from mbuild.formats.hoomd_snapshot import to_hoomdsnapshot
import numpy as np


class Ellipsoid(Compound):
    def __init__(
            self,
            name,
            mass,
            major_length,
            major_axis=[1,0,0],
            minor_length=None,
            minor_axis=None,
    ):
        super(Ellipsoid, self).__init__(name=name)
        self.major_axis = np.array(major_axis)
        self.minor_axis = np.array(minor_axis)
        self.major_length = major_length
        self.minor_length = minor_length
        n_particles = 2
        if minor_length and minor_axis:
            n_particles = 4 
        
        # Create the constituent particles
        self.head = Compound(
                pos=self.major_axis*self.major_length/2,
                name="CH",
                mass=mass/n_particles
        )
        self.tail = Compound(
                pos=-self.major_axis*self.major_length/2,
                name="CT",
                mass=mass/n_particles
        )
        self.add([self.head, self.tail])
        
        if minor_length and minor_axis:
            self.right = Compound(
                    pos=self.minor_axis*self.minor_length/2,
                    name="CR",
                    mass=mass/n_particles
            )
            self.left = Compound(
                    pos=-self.minor_axis*self.minor_length/2,
                    name="CL",
                    mass=mass/n_particles
            )
            self.add([self.right, self.left])


class Polymer(Polymer):
    def __init__(self):
        super(Polymer, self).__init__()
    
    def add_bead(self, bead, bond_axis, separation):
        particle_names = [p.name for p in bead.particles()]
        if bond_axis.lower() == "major":
            tail_idx = np.where(np.array(particle_names) == "CT")[0][0]
            head_idx = np.where(np.array(particle_names) == "CH")[0][0]
            orientation = [bead.major_axis, -bead.major_axis]
        elif bond_axis.lower() == "minor":
            tail_idx = np.where(np.array(particle_names) == "CL")[0][0]
            head_idx = np.where(particle_names == "CR")[0][0]
            orientation = [bead.minor_axis, -bead.minor_axis]
        
        self.add_monomer(
            bead, [head_idx, tail_idx], separation, orientation, replace=False
        )

