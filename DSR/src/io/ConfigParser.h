#pragma once

#include <string>
#include <nlohmann/json.hpp>
#include <iostream>
#include <docopt/docopt.h>
#include "../Parameters.h"
#include "../Settings.h"

namespace snspd::io {
  class ConfigParser {
    nlohmann::json m_config;
    Parameters m_param;
    const Settings m_settings;

    [[nodiscard]] static nlohmann::json get_config(const std::string &path);
    [[nodiscard]] static nlohmann::json get_config(const std::map<std::string, docopt::value> &args);
    [[nodiscard]] static Parameters init_params(const nlohmann::json &config);
    [[nodiscard]] static Settings init_settings(const nlohmann::json &config,
                                                const std::map<std::string, docopt::value> &args);
    [[nodiscard]] static std::vector<double> get_param_vector(const std::string &name, const nlohmann::json &config);
    [[nodiscard]] static double update_scalar(const std::string &name, double current, std::size_t step,
                                              const nlohmann::json &config);
    static void update_vector(const std::string &name, std::vector<double> &vec, std::size_t step,
                              const nlohmann::json &config);

  public:
    explicit ConfigParser(const std::string &path):
      m_config(get_config(path)),
      m_param(init_params(m_config)),
      m_settings(init_settings(m_config, std::map<std::string, docopt::value>{})) {

    }

    explicit ConfigParser(const std::map<std::string, docopt::value> &args):
      m_config(get_config(args)),
      m_param(init_params(m_config)),
      m_settings(init_settings(m_config, args)) {

    }

    [[nodiscard]] Parameters& get_params() {
      return m_param;
    };

    void update_params(unsigned int step);

    [[nodiscard]] const Settings& get_settings() const {
      return m_settings;
    }

    [[nodiscard]] nlohmann::json& get_json_config() {
      return m_config;
    }
  };
}
