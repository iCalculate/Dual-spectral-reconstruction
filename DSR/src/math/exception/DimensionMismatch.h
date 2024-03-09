#pragma once

#include <string>
#include <exception>

namespace snspd::math {
  struct DimensionMismatch : public std::exception {
    std::string message{"Initialization is already called."};

    DimensionMismatch() = default;

    explicit DimensionMismatch(std::string t_message):
      message(std::move(t_message)) {

    }

    [[nodiscard]] const char* what() const noexcept override {
      return message.c_str();
    }
  };
}
