#pragma once

#include <string>
#include <exception>

namespace snspd::io {
  struct FileNotFound : public std::exception {
    std::string message{"File not found."};

    FileNotFound() = default;

    explicit FileNotFound(std::string t_message):
        message(std::move(t_message)) {

    }

    [[nodiscard]] const char* what() const noexcept override {
      return message.c_str();
    }
  };
}
