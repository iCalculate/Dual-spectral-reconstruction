#pragma once

#include <vector>

namespace snspd::math {
  template <typename T>
  class TridiagonalLuMatrix {

    // Size of the matrix
    std::size_t m_size;

    std::vector<T>
        // Upper row in the U matrix
        m_upper,

        // Inverse diagonal of the U matrix
        m_upper_diag_inv,

        // Lower row in the L matrix
        m_lower;

  public:

    TridiagonalLuMatrix(std::vector<T> upper, std::vector<T> upper_diag_inv, std::vector<T> lower):
        m_size(upper_diag_inv.size()),
        m_upper(std::move(upper)),
        m_upper_diag_inv(std::move(upper_diag_inv)),
        m_lower(std::move(lower)) {

    }

    // Solves the vector equation Ax = b, where A is this matrix.
    std::vector<T> solve(const std::vector<T> &b) const {
      std::vector<T> x(m_size);

      // First solve the system Ly = b
      x.at(0) = b.at(0);
      for (std::size_t i = 1; i < m_size; ++i) {
        x.at(i) = b.at(i) - m_lower.at(i - 1) * x.at(i - 1);
      }

      // Solve the system Ux = y
      x.at(m_size - 1) *= m_upper_diag_inv.at(m_size - 1);
      for (std::size_t i = m_size - 1; i-- > 0;) {
        x.at(i) = (x.at(i) - m_upper.at(i) * x.at(i + 1)) * m_upper_diag_inv.at(i);
      }

      return x;
    }
  };
}
