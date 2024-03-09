#include <chrono>
#include <fstream>
#include <filesystem>
#include <fmt/format.h>
#include <fmt/chrono.h>
#include <fmt/ranges.h>
#include <spdlog/spdlog.h>
#include <random>
#include "ConfigParser.h"
#include "exception/FileNotFound.h"
#include "../exception/NotImplemented.h"

nlohmann::json snspd::io::ConfigParser::get_config(const std::string &path) {

  spdlog::debug("Reading config from {}", path);

  // Make sure that the file exists
  if (!std::filesystem::exists(path)) {
    throw FileNotFound(fmt::format("JSON config file {} does not exist.", path));
  }

  std::ifstream json_file(path);
  nlohmann::json out;
  json_file >> out;
  return out;
}

nlohmann::json snspd::io::ConfigParser::get_config(const std::map<std::string, docopt::value> &args) {

  // Path to the config file
  std::string path = args.at("--config").asString();

  return get_config(path);
}

snspd::Parameters snspd::io::ConfigParser::init_params(const nlohmann::json &config) {

  // Get the initial config values
  auto init_config = config["parameters"];

  // Get the system size
  std::size_t size{init_config["size"].get<std::size_t>()};

  spdlog::debug("Creating parameter struct.");
  Parameters params {
      0,
      init_config["maxSteps"].get<unsigned int>(),
      init_config["average"].get<unsigned int>(),
      0,
      size,
      init_config["dt"],
      init_config["q"],
      init_config["c0"],
      init_config["r"],
      init_config["vg"],
      init_config["nl"],
      init_config["i"],
      init_config["ib"],
      init_config["vb"],
      init_config["rt"],
      init_config["rs"],
      init_config["cs"],
      get_param_vector("ic", config),
      get_param_vector("x", config),
      get_param_vector("v", config),
      get_param_vector("rqp", config)
  };

  return params;
}

snspd::Settings
snspd::io::ConfigParser::init_settings(const nlohmann::json &config, const std::map<std::string, docopt::value> &args) {

  // Silent mode
  bool silent = args.at("--silent").asBool() || (config.contains("settings")
                                                 && config["settings"].contains("silent") && config["settings"]["silent"].get<bool>());

  // Save phase slips
  bool save_phase_slips = config.contains("settings") && config["settings"].contains("savePhaseSlips")
                          && config["settings"]["savePhaseSlips"].get<bool>();

  std::string output;

  // Check if the output is given as a CLI param
  if (args.at("--output")) {
    output = args.at("--output").asString();
  }

    // Check if config sets the output
  else if (config.contains("settings") && config["settings"].contains("output")) {
    output = config["settings"]["output"].get<std::string>();
  }

  else {
    output = "out_{:%Y-%m-%d-%H%M%S}.h5";
  }

  // Get current time
  auto now = std::chrono::system_clock::now();
  time_t tt = std::chrono::system_clock::to_time_t(now);
  tm local_tm = *localtime(&tt);

  Settings settings {
      fmt::format(output, local_tm),
      silent,
      save_phase_slips
  };

  return settings;
}

std::vector<double> snspd::io::ConfigParser::get_param_vector(const std::string &name, const nlohmann::json &config) {

  auto inital_config = config["parameters"];
  auto vec = inital_config[name];

  // Get the system size
  std::size_t size{inital_config["size"].get<std::size_t>()};

  // Create the object to be returned
  std::vector<double> out(size);

  // Fill the vector with a number if a scalar is given
  if (vec.is_number()) {

    spdlog::debug("Filling {} with {}.", name, vec.get<double>());

    std::fill(out.begin(), out.end(), vec.get<double>());
  }

    // Fill the vector with the array values if an array is given
  else if (vec.is_array()) {

    spdlog::debug("Setting {} to {}.", name, vec.get<std::vector<double>>());

    out = vec.get<std::vector<double>>();
  }

  // Use the options to fill the array
  else if (vec.is_object()) {

    // Value is set
    if (vec.contains("value")) {

      spdlog::debug("Filling {} with {}.", name, vec["value"].get<double>());

      std::fill(out.begin(), out.end(), vec["value"].get<double>());
    }

    // If it has stationaryPhase set to true than fill with vector that makes the phases stationary
    else if (vec.contains("stationaryPhase") && vec["stationaryPhase"].get<bool>() && name == "x") {

      spdlog::debug("Setting {} to a stationary phase.", name);

      std::size_t multiplier{size};
      double arcsin_ratio{std::asin(std::min(inital_config["i"].get<double>(), 1.0))};

      std::generate(out.begin(), out.end(), [&]() {
        return static_cast<double>(multiplier--) * arcsin_ratio;
      });
    }

    // If it has random set to true then fill with random values between min and max
    else if (vec.contains("random") && vec["random"].get<bool>()) {

      spdlog::debug("Setting {} to uniform random values in the interval [{}, {}],", name,
                    vec["min"].get<double>(), vec["max"].get<double>());

      std::random_device uniform_rnd_dev;
      std::mt19937 uniform_rnd_gen(uniform_rnd_dev());
      std::uniform_real_distribution<double> uniform_dist(vec["min"].get<double>(), vec["max"].get<double>());

      std::generate(out.begin(), out.end(), [&](){
        return uniform_dist(uniform_rnd_gen);
      });
    }

    // Set specific values
    if (vec.contains("values") && vec["values"].is_array()) {
      for (const auto &element : vec["values"]) {
        if (element.contains("index") && element.contains("value")) {
          spdlog::debug("Setting {}[{}] to {}.", name, element["index"].get<std::size_t>(),
                        element["value"].get<double>());
          out.at(element["index"].get<std::size_t>()) = element["value"].get<double>();
        }
      }
    }

  }

    // No method found
  else {
    throw NotImplemented("The selected method for filling the vector is not implemented.");
  }

  return out;
}

void snspd::io::ConfigParser::update_params(unsigned int step) {

  // Update the step
  m_param.step = step;

  // Update the time step
  ++m_param.time_step;

  // Update scalars
  m_param.nl = update_scalar("nl", m_param.nl, step, m_config);
  m_param.i = update_scalar("i", m_param.i, step, m_config);
  m_param.ib = update_scalar("ib", m_param.ib, step, m_config);
  m_param.vb = update_scalar("vb", m_param.vb, step, m_config);

  // Update vectors
  update_vector("x", m_param.x, step, m_config);
  update_vector("v", m_param.v, step, m_config);
  update_vector("ic", m_param.ic, step, m_config);
  update_vector("rqp", m_param.rqp, step, m_config);
}

double snspd::io::ConfigParser::update_scalar(const std::string &name, double current, std::size_t step,
                                              const nlohmann::json &config) {

  // Do not update the parameters if the update section is missing
  if (!config.contains("updates")) {
    return current;
  }

  auto updates = config["updates"];

  auto result = std::find_if(updates.begin(), updates.end(), [&](const nlohmann::json &update) {
    return update["values"].contains(name) && update["start"].get<std::size_t>() <= step
           && update["end"].get<std::size_t>() >= step;
  });

  if (result != updates.end()) {
    auto start = (*result)["start"].get<std::size_t>();
    auto end = (*result)["end"].get<std::size_t>();
    auto from = (*result)["values"][name]["from"].get<double>();
    auto to = (*result)["values"][name]["to"].get<double>();

    return (to - from) * (static_cast<double>(step - start)) / static_cast<double>(end - start) + from;
  }

  return current;
}

void snspd::io::ConfigParser::update_vector(const std::string &name, std::vector<double> &vec, std::size_t step,
                                            const nlohmann::json &config) {

  // Do not update the parameters if the update section is missing
  if (!config.contains("updates")) {
    return;
  }

  auto updates = config["updates"];

  auto result = std::find_if(updates.begin(), updates.end(), [&](const nlohmann::json &update) {
    return update["values"].contains(name) && update["start"].get<std::size_t>() <= step
           && update["end"].get<std::size_t>() >= step;
  });

  if (result != updates.end()) {
    auto start = (*result)["start"].get<std::size_t>();
    auto end = (*result)["end"].get<std::size_t>();

    for (const auto &update : (*result)["values"][name]) {
      auto from = update["from"].get<double>();
      auto to = update["to"].get<double>();

      // If index is a list
      if (update.contains("index") && update["index"].is_array()) {

        for (const auto &element : update["index"]) {
          auto index = element.get<std::size_t>();
          vec.at(index) = (to - from) * (static_cast<double>(step - start)) / static_cast<double>(end - start) + from;
        }

        continue;
      }

      // If index is not a list
      if (update.contains("index")) {
        auto index = update["index"].get<std::size_t>();
        vec.at(index) = (to - from) * (static_cast<double>(step - start)) / static_cast<double>(end - start) + from;
        continue;
      }

      // If a range is specified
      if (update.contains("range") && update["range"].is_array() && update["range"].size() == 2) {

        for (auto i = update["range"].at(0).get<std::size_t>();
             i < update["range"].at(1).get<std::size_t>() + 1; ++i) {
          vec.at(i) = (to - from) * (static_cast<double>(step - start)) / static_cast<double>(end - start) + from;
        }

        continue;
      }

      spdlog::warn("No index or range specified in {}. Skipping update.", name);
    }
  }
}
