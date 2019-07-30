"""
Unit and regression test for the mc_lj_potential package.
"""

# Import package, test suite, and other packages as needed
import mc_lj_potential
import pytest
import sys
import os


# Dependencies
import numpy as np

def test_num_particles():
    """
    Test if the property of num_particles is true.
    """

    coordinates = mc_lj_potential.generate_initial_state(method = 'random', num_particles = 100, box_length = 10.0 )
    mcs = mc_lj_potential.Box(coordinates = coordinates, box_length = 10.0)

    assert mcs.num_particles == 100

def test_volume():
    coordinates = mc_lj_potential.generate_initial_state(method = 'random', num_particles = 100, box_length = 5.0 )
    mcs = mc_lj_potential.Box(coordinates = coordinates, box_length = 5.0)

    assert mcs.volume == 125

def test_mc_lj_potential_imported():
    """
    Sample test, will always pass so long as import statement worked.
    """
    assert "mc_lj_potential" in sys.modules

def test_generate_initial_state_coords():
    """
    Test the coordinates generated by random method, will always pass as long as generated coordinates value is acceptsble.
    """
    np.random.seed(123)
    coordinates = mc_lj_potential.generate_initial_state("random", num_particles = 100, box_length = 10.0)
    try:
        assert np.isclose(coordinates[0][0], -6.46469)
    finally:
        np.random.seed()
    
def test_generate_intial_state_length():
    """
    Test the number of coordinates generated by generate_initial_state() function is the same as required.
    """
    coordinates = mc_lj_potential.generate_initial_state("random", num_particles = 100, box_length = 10.0)
    assert len(coordinates) == 100


def test_get_particle_energy_cutoff():
    """
    Test the get_particle_energy() function when the particle is exceed the cutoff.
    """
    coordinates = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,4.0])]
    box_length = 10.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = 3.0)
    expected_vaule = 0.0
    calculated_value = mcs.get_particle_energy(0)
    assert np.isclose(expected_vaule, calculated_value)

def test_get_particle_energy_equi():
    """
    Test the get_paricle_energy() function when it is at the equilibrated point.
    """
    coordinates = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,1.0])]
    box_length = 10.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = 3.0)
    expected_vaule = 0.0
    calculated_value = mcs.get_particle_energy(0)
    assert np.isclose(expected_vaule, calculated_value)

def test_lennard_jones_potential():
    """
    Test the definition of lennard_jones_potential() function. It will pass when the calculated potential is equal to actual potential defined by lennard jones.
    """
    coordinates = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,1.0])]
    box_length = 10.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = 3.0)
    expected_vaule = 224.0
    calculated_value = mcs.lennard_jones_potential(0.5)
    assert np.isclose(expected_vaule, calculated_value)

@pytest.fixture
def mcs():
    """
    Set up the fixture to have a general MCState that can be callable for all tests of different energy functions.
    """ 
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "sample_config.xyz")
    coordinates = mc_lj_potential.generate_initial_state(method = "file", file_name=file_path)
    box_length = 10.0
    cutoff = 3.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = cutoff)
    return mcs

def test_calculate_total_pair_energy(mcs):
    """
    Test calculate_total_pair_energy() function, will pass if the calcualted total pair energy is equal to the reported energy of the system.
    """
    calculated_pair_energy = mcs.calculate_total_pair_energy()
    assert np.isclose(calculated_pair_energy, -4.3515E+03)

def test_calculate_tail_correction(mcs):
    """
    Test calculate_tail_correction() function, will pass if the calcualted tail correction is equal to the expected tail correction of the system.
    """
    calculated_tail_correction = mcs.calculate_tail_correction()
    assert np.isclose(calculated_tail_correction, -198.488258)

def test_get_particle_energy(mcs):
    """
    Test get_particle_energy() function, will pass if the calcualted particle energy is equal to the reported energy of the choosed particle.
    """
    calculated_particle_energy = mcs.get_particle_energy(0)
    assert np.isclose(calculated_particle_energy, -10.877945)

def test_calculate_unit_energy(mcs):
    """
    Test calculate_unit_energy() function, will pass if the calcualted unit energy is equal to the expected value.
    """
    total_pair_energy = mcs.calculate_total_pair_energy()
    tail_correction = mcs.calculate_tail_correction()
    calculated_unit_energy = mcs.calculate_unit_energy()
    assert np.isclose(calculated_unit_energy, (total_pair_energy + tail_correction)/800)

def test_accpet_or_reject_true():
    """
    Test the accept_or_reject function when it is true.
    """
    expected_vaule1 = True
    calculated_value1 = mc_lj_potential.accept_or_reject(-1.0,0.10)
    assert expected_vaule1 == calculated_value1

def test_accpet_or_reject_false():
    """
    Test the accept_or_reject function when it is False.
    """
    np.random.seed(10)
    expected_vaule2 = False
    calculated_value2 = mc_lj_potential.accept_or_reject(6.0, 0.10)
    try:
        assert expected_vaule2 == calculated_value2
    finally:
        np.random.seed()

def test_accpet_or_reject_true_ran():
    """
    Test the accept_or_reject function when energy increase but it is still accepted.
    """
    np.random.seed(354)
    expected_vaule3 = True
    calculated_value3 = mc_lj_potential.accept_or_reject(0.1, 0.10)
    try:
         assert expected_vaule3 == calculated_value3
    finally:
         np.random.seed()

def test_adjust_displacement_large():
    """
    Test the accept_or_reject function when the movement is too large that the max_displacement should be changed into a smaller value.
    """
    n_trials = 100.0
    n_accept = 37.0
    max_displacement = 1.0
    expected_vaule = 0.8

    cal_max_displacement, n_trials, n_accept = mc_lj_potential.adjust_displacement(n_trials = n_trials, n_accept = n_accept, max_displacement = max_displacement)
    assert expected_vaule == cal_max_displacement

def test_adjust_displacement_fit():
    """
    Test the accept_or_reject function when the movement is suitable, will pass the max_displacement is kept.
    """
    n_trials = 100.0
    n_accept = 40.0
    max_displacement = 1.0
    expected_value = 1.0   

    cal_max_displacement, n_trials, n_accept = mc_lj_potential.adjust_displacement(n_trials = n_trials, n_accept = n_accept, max_displacement = max_displacement)
    assert expected_value == cal_max_displacement

def test_adjust_displacement_small():
    """
    Test the accept_or_reject function when the movement is too small, will pass the max_displacement is increased.
    """
    n_trials = 100.0
    n_accept = 43.0
    max_displacement = 1.0
    expected_value = 1.2   

    cal_max_displacement, n_trials, n_accept = mc_lj_potential.adjust_displacement(n_trials = n_trials, n_accept = n_accept, max_displacement = max_displacement)
    assert expected_value == cal_max_displacement
