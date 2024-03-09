#pragma once

#include <string>

namespace snspd {
  struct Settings {
    std::string output;
    bool silent;
    bool save_phase_slips;
  };
}
