#pragma once

#include <random>
#include "Parameters.h"
#include "event/EventStorage.h"

namespace snspd {
  class Model {
    Parameters &m_param;

    event::EventStorage &m_storage;

    const math::TridiagonalMatrix<double> m_mass;

    std::random_device m_rnd_dev;
    std::mt19937 m_rnd_gen;
    std::normal_distribution<double> m_rnd_dist;

    // The difference between phases
    std::vector<long int> m_branch;

    // Generate random vector with a specified length and amplitude.
    // The random numbers have zero mean and standard deviation amplitude
    std::vector<double> generate_rnd_vector(double amplitude, std::size_t length);

    // Generate the mass matrix M
    [[nodiscard]] static math::TridiagonalMatrix<double> generate_mass_matrix(const Parameters &param);

    // Generate the matrix A
    [[nodiscard]] static math::TridiagonalMatrix<double> generate_alpha_matrix(const Parameters &param);

    // Get the resistance
    [[nodiscard]] static double get_resistance(const Parameters &param, std::size_t site);

    // Get the voltage
    [[nodiscard]] static double get_voltage(const Parameters &param, std::size_t site);

    // Get the force
    [[nodiscard]] std::vector<double> get_force_damping(const Parameters &param,
                                                        const math::TridiagonalMatrix<double> &alpha);

    [[nodiscard]] static std::vector<long int> get_branch(const std::vector<double> &x);

  public:
    explicit Model(Parameters &param, event::EventStorage &storage):
      m_param(param),
      m_storage(storage),
      m_mass(generate_mass_matrix(param)),
      m_rnd_gen(m_rnd_dev()),
      m_rnd_dist(0.0, 1.0),
      m_branch(get_branch(param.x)) {

    }

    // Take one time step
    void run();
  };
}


