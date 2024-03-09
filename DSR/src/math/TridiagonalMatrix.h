
#pragma once

#include <vector>
#include <stdexcept>
#include <cmath>
#include "TridiagonalLuMatrix.h"
#include "VectorOperations.h"
#include "exception/DimensionMismatch.h"

namespace snspd::math {

  template <typename T>
  class TridiagonalMatrix {
    std::size_t m_size;

    std::vector<T>
        m_diagonal,
        m_upper,
        m_lower;

  public:

    // Enum for selecting a diagonal
    constexpr static int
        DIAG = 0,
        UPPER = 1,
        LOWER = -1;

    // Create an empty tridiagonal matrix with specified size.
    explicit TridiagonalMatrix(std::size_t size):
        m_size(size),
        m_diagonal(size),
        m_upper(size - 1),
        m_lower(size - 1) {

    }

    TridiagonalMatrix(std::vector<T> diagonal, std::vector<T> upper, std::vector<T> lower):
        m_size(diagonal.size()),
        m_diagonal(std::move(diagonal)),
        m_upper(std::move(upper)),
        m_lower(std::move(lower)) {

    }

    static TridiagonalMatrix<T> eye(std::size_t size) {
      return TridiagonalMatrix(std::vector<T>(size, 1.0), std::vector<T>(size - 1), std::vector<T>(size - 1));
    }

    // Get the size of the matrix
    [[nodiscard]] std::size_t size() const {
      return m_size;
    }

    // Get one of the diagonals
    const std::vector<T> &get_diagonal(int diag) const {
      switch (diag) {
        case DIAG:
          return m_diagonal;

        case UPPER:
          return m_upper;

        case LOWER:
          return m_lower;

        default:
          throw DimensionMismatch("The diag must be DIAG (=0), UPPER (=1) or LOWER (=-1)");
      }
    }

    // Get one of the diagonals (non-const version)
    std::vector<T> &get_diagonal(int diag) {
      return const_cast<std::vector<T>&>(const_cast<const TridiagonalMatrix<T>*>(this)->get_diagonal(diag));
    }

    // Set one diagonal
    void set_diagonal(int diag, std::vector<T> value) {
      std::vector<T> &diagonal = get_diagonal(diag);

      // Make sure that the length of the new diagonal is the same as the old one
      if (diagonal.size() != value.size()) {
        throw DimensionMismatch("The assigned value must have the same length as the existing diagonal.");
      }

      diagonal = std::move(value);
    }

    // Fill one of the diagonals with the same value
    void fill_diagonal(int diag, T value) {
      std::vector<T> &diagonal = get_diagonal(diag);

      std::fill(diagonal.begin(), diagonal.end(), value);
    }

    // Get one component of the matrix
    [[nodiscard]] T get(int diag, std::size_t index) const {
      std::vector<T> &diagonal = get_diagonal(diag);
      return diagonal.at(index);
    }

    // Set one component of the matrix
    void set(int diag, std::size_t index, T value) {
      std::vector<T> &diagonal = get_diagonal(diag);
      diagonal.at(index) = value;
    }

    // LU factorization of matrix
    [[nodiscard]] TridiagonalLuMatrix<T> lu_factorize() {
      std::vector<T>
          lu_upper_diag_inv(m_size),
          lu_lower(m_size - 1),
          lu_upper(m_upper);

      lu_upper_diag_inv.at(0) = 1 / m_diagonal.at(0);

      for (std::size_t i = 1; i < m_size; ++i) {
        lu_lower.at(i - 1) = m_lower.at(i - 1) * lu_upper_diag_inv.at(i - 1);
        lu_upper_diag_inv.at(i) = 1 / (m_diagonal.at(i) - m_upper.at(i - 1) * lu_lower.at(i - 1));
      }

      return TridiagonalLuMatrix<T>(lu_upper, lu_upper_diag_inv, lu_lower);
    }

    // Compute the Frobenius norm squared of the matrix
    [[nodiscard]] double norm_squared() const {
      return math::norm_squared(m_diagonal) + math::norm_squared(m_upper) + math::norm_squared(m_lower);
    }

    // Compute the Frobenius norm of the matrix
    [[nodiscard]] double norm() const {
      return std::sqrt(norm_squared());
    }

    // Allow matrix addition
    [[nodiscard]] friend TridiagonalMatrix<T> operator+(const TridiagonalMatrix<T> &lhs,
                                                        const TridiagonalMatrix<T> &rhs) {

      // Make sure that the size is correct
      if (lhs.m_size != rhs.m_size) {
        throw DimensionMismatch("Matrices need to have the same size.");
      }

      TridiagonalMatrix<T> output(lhs.m_size);

      for (std::size_t i = 0; i < lhs.m_size; ++i) {
        output.m_diagonal.at(i) = lhs.m_diagonal.at(i) + rhs.m_diagonal.at(i);
      }

      for (std::size_t i = 0; i < lhs.m_size - 1; ++i) {
        output.m_upper.at(i) = lhs.m_upper.at(i) + rhs.m_upper.at(i);
      }

      for (std::size_t i = 0; i < lhs.m_size - 1; ++i) {
        output.m_lower.at(i) = lhs.m_lower.at(i) + rhs.m_lower.at(i);
      }

      return output;
    }

    // Assign add
    void operator+=(const TridiagonalMatrix<T> &mat) {

      // Make sure that the size is correct
      if (m_size != mat.m_size) {
        throw DimensionMismatch("Matrices need to have the same size.");
      }

      for (std::size_t i = 0; i < m_size; ++i) {
        m_diagonal.at(i) += mat.m_diagonal.at(i);
      }

      for (std::size_t i = 0; i < mat.m_size - 1; ++i) {
        m_upper.at(i) += mat.m_upper.at(i);
      }

      for (std::size_t i = 0; i < mat.m_size - 1; ++i) {
        m_lower.at(i) += mat.m_lower.at(i);
      }
    }

    // Allow matrix subtraction
    [[nodiscard]] friend TridiagonalMatrix<T> operator-(const TridiagonalMatrix<T> &lhs,
                                                        const TridiagonalMatrix<T> &rhs) {

      // Make sure that the size is correct
      if (lhs.m_size != rhs.m_size) {
        throw DimensionMismatch("Matrices need to have the same size.");
      }

      TridiagonalMatrix<T> output(lhs.m_size);

      for (std::size_t i = 0; i < lhs.m_size; ++i) {
        output.m_diagonal.at(i) = lhs.m_diagonal.at(i) - rhs.m_diagonal.at(i);
      }

      for (std::size_t i = 0; i < lhs.m_size - 1; ++i) {
        output.m_upper.at(i) = lhs.m_upper.at(i) - rhs.m_upper.at(i);
      }

      for (std::size_t i = 0; i < lhs.m_size - 1; ++i) {
        output.m_lower.at(i) = lhs.m_lower.at(i) - rhs.m_lower.at(i);
      }

      return output;
    }

    // Assign add
    void operator-=(const TridiagonalMatrix<T> &mat) {

      // Make sure that the size is correct
      if (m_size != mat.m_size) {
        throw DimensionMismatch("Matrices need to have the same size.");
      }

      for (std::size_t i = 0; i < m_size; ++i) {
        m_diagonal.at(i) -= mat.m_diagonal.at(i);
      }

      for (std::size_t i = 0; i < mat.m_size - 1; ++i) {
        m_upper.at(i) -= mat.m_upper.at(i);
      }

      for (std::size_t i = 0; i < mat.m_size - 1; ++i) {
        m_lower.at(i) -= mat.m_lower.at(i);
      }
    }

    // Matrix scalar multiplication
    [[nodiscard]] friend TridiagonalMatrix<T> operator*(const TridiagonalMatrix<T> &mat, const T &scalar) {

      TridiagonalMatrix<T> output(mat.m_size);

      for (std::size_t i = 0; i < mat.m_size; ++i) {
        output.m_diagonal.at(i) = mat.m_diagonal.at(i) * scalar;
      }

      for (std::size_t i = 0; i < mat.m_size - 1; ++i) {
        output.m_upper.at(i) = mat.m_upper.at(i) * scalar;
      }

      for (std::size_t i = 0; i < mat.m_size - 1; ++i) {
        output.m_lower.at(i) = mat.m_lower.at(i) * scalar;
      }

      return output;
    }

    // Matrix scalar multiplication
    [[nodiscard]] friend TridiagonalMatrix<T> operator*(const T &scalar, const TridiagonalMatrix<T> &mat) {
      return mat * scalar;
    }

    // Matrix scalar multiplication assign
    void operator*(const T &scalar) {
      for (std::size_t i = 0; i < m_size; ++i) {
        m_diagonal.at(i) *= scalar;
      }

      for (std::size_t i = 0; i < m_size - 1; ++i) {
        m_upper.at(i) *= scalar;
      }

      for (std::size_t i = 0; i < m_size - 1; ++i) {
        m_lower.at(i) *= scalar;
      }
    }

    // Matrix vector multiplication
    [[nodiscard]] friend std::vector<T> operator*(const TridiagonalMatrix<T> &mat, const std::vector<T> &vec) {

      if (mat.m_size != vec.size()) {
        throw DimensionMismatch("Matrix and vector needs to have the same size to multiply.");
      }

      std::vector<T> res(mat.m_size);

      res.at(0) = mat.m_diagonal.at(0) * vec.at(0) + mat.m_upper.at(0) * vec.at(1);

      for (std::size_t i = 1; i < mat.m_size - 1; ++i) {
        res.at(i) = mat.m_lower.at(i - 1) * vec.at(i - 1) + mat.m_diagonal.at(i) * vec.at(i)
            + mat.m_upper.at(i) * vec.at(i + 1);
      }

      res.at(mat.m_size - 1) = mat.m_lower.at(mat.m_size - 2) * vec.at(mat.m_size - 2)
          + mat.m_diagonal.at(mat.m_size - 1) * vec.at(mat.m_size - 1);

      return res;
    }
  };
}


