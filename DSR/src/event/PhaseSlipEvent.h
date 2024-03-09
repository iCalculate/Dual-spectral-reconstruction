#pragma once

#include <cstddef>

namespace snspd::event {
  struct PhaseSlipEvent {
    unsigned int time_step;
    std::size_t location;
    long int branch;
  };
}
