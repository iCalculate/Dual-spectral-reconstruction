#include <algorithm>
#include <cmath>
#include "Model.h"
#include "math/TridiagonalLuMatrix.h"
#include "math/VectorOperations.h"

void snspd::Model::run() {

  using namespace snspd::math;

  // Update the phase to t + dt/2
  m_param.x += m_param.v * (m_param.dt / 2);

  // Get alpha
  TridiagonalMatrix<double> alpha = generate_alpha_matrix(m_param);

  // Compute the mass alpha matrix and factorize it
  TridiagonalLuMatrix<double> mass_alpha = ((m_param.dt / 2) * alpha + m_mass).lu_factorize();

  // Solve the matrix system
  auto res = mass_alpha.solve(get_force_damping(m_param, alpha));

  // Update the voltage and phase
  m_param.v += res;
  m_param.x += m_param.v * (m_param.dt / 2);

  auto new_branch = get_branch(m_param.x);

  // Check for phase slips
  for (std::size_t i = 0; i < m_param.size - 1; ++i) {

    if (m_branch.at(i) != new_branch.at(i)) {

      // Save phase slip events
      m_storage.save_phase_slip(m_param.time_step, i, new_branch.at(i));

      // Update the branch
      m_branch.at(i) = new_branch.at(i);
    }
  }
}

std::vector<double> snspd::Model::generate_rnd_vector(double amplitude, std::size_t length) {
  std::vector<double> rnd_vec(length);

  std::generate(rnd_vec.begin(), rnd_vec.end(), [&] {
    return amplitude * m_rnd_dist(m_rnd_gen);
  });

  return rnd_vec;
}

snspd::math::TridiagonalMatrix<double> snspd::Model::generate_mass_matrix(const Parameters &param) {
  using mat = math::TridiagonalMatrix<double>;

  mat mass(param.size);

  // Fill the diagonal with {(1 + c0 + cs)q^2, (2 + c0)q^2, (2 + c0)q^2, ...}.
  mass.fill_diagonal(mat::DIAG, (2 + param.c0) * param.q * param.q);
  mass.set(mat::DIAG, 0, (1 + param.c0 + param.cs) * param.q * param.q);

  // Fill the upper diagonal with {-q^2, -q^2, ...}.
  mass.fill_diagonal(mat::UPPER, -1.0 * param.q * param.q);

  // Fill the lower diagonal with {-q^2, -q^2, ...}.
  mass.fill_diagonal(mat::LOWER, -1.0 * param.q * param.q);

  return mass;
}

snspd::math::TridiagonalMatrix<double> snspd::Model::generate_alpha_matrix(const snspd::Parameters &param) {
  using mat = math::TridiagonalMatrix<double>;

  mat alpha(param.size);

  double forward_res{get_resistance(param, 0)};
  double backward_res;

  // Update first row
  alpha.set(mat::DIAG, 0, 1.0 / forward_res);
  alpha.set(mat::UPPER, 0, -1.0 / forward_res);

  // Update row i
  for (std::size_t i = 1; i < param.size - 1; ++i) {
    backward_res = forward_res;
    forward_res = get_resistance(param, i);

    alpha.set(mat::DIAG, i, 1.0 / backward_res + 1.0 / forward_res);
    alpha.set(mat::UPPER, i, -1.0 / forward_res);
    alpha.set(mat::LOWER, i - 1, -1.0 / backward_res);
  }

  // Update last row
  backward_res = forward_res;
  forward_res = get_resistance(param, param.size - 1);

  alpha.set(mat::DIAG, param.size - 1, 1.0 / forward_res + 1.0 / backward_res);
  alpha.set(mat::LOWER, param.size - 2, -1.0 / backward_res);

  return alpha;
}

double snspd::Model::get_resistance(const snspd::Parameters &param, std::size_t site) {

  // Return the normal resistance when the voltage is larger than vg
  if (std::abs(get_voltage(param, site)) >= param.vg) {
    return param.r;
  }

  return param.rqp.at(site);
}

double snspd::Model::get_voltage(const snspd::Parameters &param, std::size_t site) {

  // Last site has voltage equal to itself
  if (site == param.size - 1) {
    return param.v.at(site);
  }

  return param.v.at(site) - param.v.at(site + 1);
}

std::vector<double> snspd::Model::get_force_damping(const snspd::Parameters &param,
                                            const snspd::math::TridiagonalMatrix<double> &alpha) {

  // The resulting force
  std::vector<double> force(param.size);

  // Damping
  std::vector<double> alpha_v = alpha * param.v;

  // Noise
  // {rnd(0), rnd(1) - rnd(0), ..., rnd(n) - rnd(n - 1), -rnd(n)}
  auto rnd = generate_rnd_vector(std::sqrt(2 * param.nl * param.dt), param.size);

  // Compensate noise with the resistance
  for (std::size_t i = 0; i < rnd.size(); ++i) {
    rnd.at(i) /= std::sqrt(get_resistance(param, i));
  }

  // The difference between terms is the noise
  auto noise = math::shifted_diff(rnd, rnd);

  // Sine phase difference
  // {sin(x(0)), sin(x(1) - x(0)), ..., sin(x(n) - sin(n - 1)), sin(-x(n))}
  auto sine_diff = math::sin(math::shifted_diff(param.x, param.x));

  // Set the first component
  force.at(0) = param.dt * (param.i + param.ic.at(0) * sine_diff.at(1) - alpha_v.at(0)) - noise.at(0);

  // Set the other components
  for (std::size_t i = 1; i < param.size; ++i) {
    force.at(i) = param.dt * (-param.ic.at(i - 1) * sine_diff.at(i) + param.ic.at(i) * sine_diff.at(i + 1)
                              - alpha_v.at(i)) - noise.at(i);
  }

  return force;
}

std::vector<long int> snspd::Model::get_branch(const std::vector<double> &x) {
  std::vector<long int> branch(x.size() - 1);

  for (std::size_t i = 0; i < x.size() - 1; ++i) {
    branch.at(i) = static_cast<long int>(std::floor(((x.at(i + 1) - x.at(i)) + M_PI) / (2 * M_PI)));
  }

  return branch;
}
