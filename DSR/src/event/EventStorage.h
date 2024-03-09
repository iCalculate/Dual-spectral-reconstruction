#pragma once

#include <vector>
#include <climits>
#include <h5pp/h5pp.h>
#include "PhaseSlipEvent.h"
#include "../Settings.h"

namespace snspd::event {
  class EventStorage {
    const Settings &m_settings;

    std::vector<PhaseSlipEvent> m_phase_slips{};

  public:

    explicit EventStorage(const Settings &settings):
        m_settings(settings) {

    }

    void save_phase_slip(unsigned int time_step, std::size_t location, long int branch) {

      // Save phase slips if needed
      if (m_settings.save_phase_slips) {
        m_phase_slips.push_back(PhaseSlipEvent{
            time_step,
            location,
            branch
        });
      }
    }

    [[nodiscard]] const std::vector<PhaseSlipEvent>& get_phase_slips() const {
      return m_phase_slips;
    }

    void flush_phase_slips(h5pp::File &file) const {
      h5pp::hid::h5t H5_PHASE_SLIP = H5Tcreate(H5T_COMPOUND, sizeof(event::PhaseSlipEvent));
      H5Tinsert(H5_PHASE_SLIP, "t", HOFFSET(event::PhaseSlipEvent, time_step), H5T_NATIVE_INT);
      H5Tinsert(H5_PHASE_SLIP, "x", HOFFSET(event::PhaseSlipEvent, location), H5T_NATIVE_INT);
      H5Tinsert(H5_PHASE_SLIP, "branch", HOFFSET(event::PhaseSlipEvent, branch), H5T_NATIVE_INT);

      // Store events
      file.writeDataset(m_phase_slips, "phase_slips", H5_PHASE_SLIP);
    }
  };
}
