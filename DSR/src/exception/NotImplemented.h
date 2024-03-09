#pragma once

#include <exception>
#include <string>

namespace snspd {
  struct NotImplemented : public std::exception {
    std::string message{"Method is not implemented"};

    NotImplemented() = default;

    explicit NotImplemented(std::string t_message):
        message(std::move(t_message)) {

    }

    [[nodiscard]] const char* what() const noexcept override {
      return message.c_str();
    }
  };
}
