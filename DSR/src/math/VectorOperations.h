#pragma once

#include <vector>
#include <stdexcept>
#include <algorithm>
#include <numeric>
#include "exception/DimensionMismatch.h"

namespace snspd::math {

  // Allow vectors to be added
  template <typename T>
  [[nodiscard]] std::vector<T> operator+(const std::vector<T> &lhs, const std::vector<T> &rhs) {

    // Check that the vectors have the same length
    if (lhs.size() != rhs.size()) {
      throw DimensionMismatch("Vectors need to have the same size to be added.");
    }

    std::vector<T> res(lhs.size());

    std::transform(lhs.begin(), lhs.end(), rhs.begin(), res.begin(), std::plus<T>());

    return res;
  }

  // Allow vectors to be subtracted
  template <typename T>
  [[nodiscard]] std::vector<T> operator-(const std::vector<T> &lhs, const std::vector<T> &rhs) {

    // Check that the vectors have the same length
    if (lhs.size() != rhs.size()) {
      throw DimensionMismatch("Vectors need to have the same size to be subtracted.");
    }

    std::vector<T> res(lhs.size());

    std::transform(lhs.begin(), lhs.end(), rhs.begin(), res.begin(), std::minus<T>());

    return res;
  }

  // Add to existing vector
  template <typename T>
  std::vector<T>& operator+=(std::vector<T>& lhs, const std::vector<T>& rhs) {

    if (lhs.size() != rhs.size()) {
      throw DimensionMismatch("Vectors need to have the same size to be added.");
    }

    std::transform(lhs.begin(), lhs.end(), rhs.begin(), lhs.begin(), std::plus<T>());

    return lhs;
  }

  // Subtract from existing vector
  template <typename T>
  std::vector<T>& operator-=(std::vector<T>& lhs, const std::vector<T>& rhs) {

    if (lhs.size() != rhs.size()) {
      throw DimensionMismatch("Vectors need to have the same size to be added.");
    }

    std::transform(lhs.begin(), lhs.end(), rhs.begin(), lhs.begin(), std::minus<T>());

    return lhs;
  }

  // Allow vectors to be multiplied with a scalar
  template <typename T>
  [[nodiscard]] std::vector<T> operator*(const std::vector<T> &vec, const T &scalar) {

    std::vector<T> res(vec.size());

    std::transform(vec.begin(), vec.end(), res.begin(), std::bind1st(std::multiplies<T>(), scalar));

    return res;
  }

  // Allow vectors to be multiplied with a scalar
  template <typename T>
  [[nodiscard]] std::vector<T> operator*(const T &scalar, const std::vector<T> &vec) {
    return vec * scalar;
  }

  // Allow vectors to be divided by a scalar
  template <typename T>
  [[nodiscard]] std::vector<T> operator/(const std::vector<T> &vec, const T &scalar) {
    return vec * (1 / scalar);
  }

  // Allow vectors to be multiplied component-wise
  template <typename T>
  [[nodiscard]] std::vector<T> operator*(const std::vector<T> &lhs, const std::vector<T> &rhs) {

    if (lhs.size() != rhs.size()) {
      throw DimensionMismatch("Vectors need to have the same length when doing component-wise multiplication.");
    }

    std::vector<T> res(lhs.size());

    std::transform(lhs.begin(), lhs.end(), rhs.begin(), res.begin(), std::multiplies<T>());

    return res;
  }

  // Computes sine of a vector
  template <typename T>
  [[nodiscard]] std::vector<T> sin(const std::vector<T> &vec) {
    std::vector<T> res(vec.size());

    for (std::size_t i = 0; i < vec.size(); ++i) {
      res.at(i) = std::sin(vec.at(i));
    }

    return res;
  }

  // Computes the shifted difference of two vectors
  // The result is: (vec1[0], vec1[1] - vec2[0], vec1[2] - vec2[1], ..., -vec2[n])
  template <typename T>
  [[nodiscard]] std::vector<T> shifted_diff(const std::vector<T> &vec1, const std::vector<T> &vec2) {

    if (vec1.size() != vec2.size()) {
      throw DimensionMismatch("Vectors need to have the same length to be used in shifted difference.");
    }

    std::vector<T> res(vec1.size() + 1);

    // Get the first component
    res.at(0) = vec1.at(0);

    for (std::size_t i = 1; i < vec1.size(); ++i) {
      res.at(i) = vec1.at(i) - vec2.at(i - 1);
    }

    res.at(vec1.size()) = - vec2.at(vec1.size() - 1);

    return res;
  }

  template <typename T>
  [[nodiscard]] double norm_squared(const std::vector<T> &vec) {
    return std::inner_product(vec.begin(), vec.end(), vec.begin(), static_cast<T>(0.0));
  }

  template <typename T>
  [[nodiscard]] double norm(const std::vector<T> &vec) {
    return std::sqrt(norm_squared(vec));
  }
}
