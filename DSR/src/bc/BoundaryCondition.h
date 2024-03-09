#pragma once

#include "../Parameters.h"

namespace snspd::bc {
  class BoundaryCondition {
  protected:
    Parameters &m_param;

  public:

    explicit BoundaryCondition(Parameters &param):
        m_param(param) {

    }

    virtual ~BoundaryCondition() = default;

    // Simplest possible boundary condition
    virtual void run() {
      m_param.i = m_param.ib;
    };
  };
}
