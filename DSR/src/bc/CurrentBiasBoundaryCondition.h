#pragma once

#include "BoundaryCondition.h"

namespace snspd::bc {
  class CurrentBiasBoundaryCondition : public BoundaryCondition {
    std::random_device m_rnd_dev;
    std::mt19937 m_rnd_gen;
    std::normal_distribution<double> m_rnd_dist;
  public:

    explicit CurrentBiasBoundaryCondition(Parameters &param):
        BoundaryCondition(param),
        m_rnd_gen(m_rnd_dev()),
        m_rnd_dist(0.0, 1.0) {

    }

    // Compute the current going into the SNSPD
    // The current going through the SNSPD is given by I = I_b - V_0 / R_s - eta_s
    void run() override {

      // Compute the stochastic term
      auto noise = m_param.nl * std::sqrt(m_param.dt * m_param.rs) * m_rnd_dist(m_rnd_gen);

      m_param.i = m_param.ib - m_param.v.at(0) / m_param.rs - noise;
    }
  };
}
