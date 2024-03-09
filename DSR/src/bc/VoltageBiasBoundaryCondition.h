#pragma once

#include "BoundaryCondition.h"

namespace snspd::bc {
  class VoltageBiasBoundaryCondition : public BoundaryCondition {
    std::random_device m_rnd_dev;
    std::mt19937 m_rnd_gen;
    std::normal_distribution<double> m_rnd_dist;
  public:

    explicit VoltageBiasBoundaryCondition(Parameters &param):
        BoundaryCondition(param),
        m_rnd_gen(m_rnd_dev()),
        m_rnd_dist(0.0, 1.0) {

    }

    // Compute the current going into the SNSPD
    // The current going through the SNSPD is given by I = V_b / R_t - V_0 (1 / R_s + 1 / R_t) - eta_(s+t)
    void run() override {

      // Compute the stochastic term
      auto noise = std::sqrt(2 * m_param.nl * (1 / m_param.rs + 1 / m_param.rt) / m_param.dt)
          * m_rnd_dist(m_rnd_gen);

      m_param.i = m_param.vb / m_param.rt - m_param.v.at(0) * (1 / m_param.rs + 1 / m_param.rt) - noise;
    }
  };
}
