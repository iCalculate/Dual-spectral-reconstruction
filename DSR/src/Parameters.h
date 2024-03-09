#pragma once

#include <vector>
#include <iostream>
#include <fmt/format.h>
#include "math/TridiagonalMatrix.h"

namespace snspd {
  struct Parameters {

    // The current parameter step
    unsigned int step{0};

    unsigned int max_steps;

    unsigned int average{1};

    unsigned int time_step{0};

    // The number of segments.
    std::size_t size;

    double

        // Length of a time step measured in units of L_K/R.
        dt,

        // Quality factor R \sqrt(C / L).
        q,

        // Capacitance to ground in terms of the capacitance C.
        c0,

        // Resistance measured in terms of the resistance R.
        r,

        // Cut-off voltage in terms of R I_c.
        // Below this voltage the resistance is given by rqp.
        // Above this voltage the resistance is given by 1 (= R / R).
        vg,

        // Noise level given by \sqrt(2 k_B T / (R I_c^2)).
        nl,

        // Current going into the SNSPD. Measured in terms of the critical current I_c.
        i,

        // Bias current in terms of the critical current I_c.
        // Used when current bias is used.
        ib,

        // Bias voltage in terms of R I_c.
        // Used when voltage bias is used.
        vb,

        // Resistance in series with the SNSPD. Measured in terms of the resistance R.
        // Used when voltage bias is used.
        rt,

        // Resistor shunting the SNSPD. Measured in terms of the resistance R.
        // Used when current or voltage bias is used.
        rs,

        // Capacitance shunting the SNSPD. Measured in units of the capacitance C.
        // Applied by increasing the capacitance on the first node and is therefore active for all boundary conditions.
        // Set to zero to disable.
        cs;

    std::vector<double>

        // Critical current that can vary across the nanowire.
        // Measured in terms of I_c, i.e. 1 corresponds to normal critical current and values less than 1 corresponds to
        // a reduced critical current.
        ic,

        // The phase at each site.
        x,

        // The voltage at each site.
        v,

        // Quasiparticle resistance in terms of the resistance R.
        // The resistance can take different values for each site.
        rqp;
  };

  // Make it possible to print parameters
  inline std::ostream& operator<<(std::ostream &os, const snspd::Parameters &params) {
    os
      << "Time:               "       << static_cast<double>(params.time_step) * params.dt  << '\n'
      << "Time step:          "       << params.time_step                                   << '\n'
      << "\u0394t:                 "  << params.dt                                          << '\n'
      << "Size:               "       << params.size                                        << '\n'
      << "Quality:            "       << params.q                                           << '\n'
      << "Ground capacitance: "       << params.c0                                          << '\n'
      << "Cut-off voltage:    "       << params.vg                                          << '\n'
      << "Noise level:        "       << params.nl                                          << '\n'
      << "Bias current:       "       << params.ib                                          << '\n'
      << '\n'
      << "| Site |      Phase |    Voltage | Critical current | Quasiparticle resistance |";

    for (std::size_t i = 0; i < params.size; ++i) {
      os
        << '\n'
        << fmt::format("| {:>4} | {:>10.2f} | {:>10.2f} | {:>16.2f} | {:>24.2f} |", i, params.x.at(i),
                       params.v.at(i), params.ic.at(i), params.rqp.at(i));
    }

    os << '\n';

    return os;
  }
}
