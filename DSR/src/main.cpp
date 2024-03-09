#include <docopt/docopt.h>
#include <spdlog/spdlog.h>
#include <indicators/progress_bar.hpp>
#include "Model.h"
#include "io/ConfigParser.h"
#include "io/Exporter.h"
#include "bc/BoundaryConditionFactory.h"
#include "event/EventStorage.h"

static constexpr auto USAGE = R"(
SNSPD simulation using the non-linear resistive and capacitive shunted junction model

Usage:
  snspd-rcsj [options]

Options:
  -h, --help              Show the help screen.
  -V, --version           Display the version.
  -v, --verbose           Run program in verbose mode.
  -s, --silent            Run program in silent mode (without progress bar).
  -c, --config=<CONFIG>   Path to the JSON config file [default: settings.json].
  -o, --output=<OUTPUT>   HDF5 file to store output data.
)";

int main(int argc, char *argv[]) {

  using namespace snspd;
  using namespace indicators;

  auto args = docopt::docopt(USAGE,{ std::next(argv), std::next(argv, argc) },true,"v1.0.0");

  // Check if verbose logging should be enabled
  if (args.at("--verbose").asBool()) {
    spdlog::set_level(spdlog::level::debug);
    spdlog::debug("Verbose mode enabled.");
  }

  // Get the config parser;
  io::ConfigParser config(args);

  // Get the event storage
  event::EventStorage storage(config.get_settings());

  // Get the exporter
  io::Exporter exporter(config, storage);

  // Get the model
  Model model(config.get_params(), storage);

  // Get the boundary conditions
  auto boundary_condition = bc::BoundaryConditionFactory::make(config);

  // Progress bar
  ProgressBar bar{
      option::BarWidth{50},
      option::Start{"["},
      option::Fill{"="},
      option::Lead{">"},
      option::Remainder{" "},
      option::End{"]"},
      option::ForegroundColor{Color::white},
      option::FontStyles{std::vector<FontStyle>{FontStyle::bold}},
      option::ShowPercentage{true},
      option::ShowElapsedTime{true},
      option::ShowRemainingTime{true}
  };

  for (unsigned int i = 0; i < config.get_params().max_steps; ++i) {

    // Check if progress bar is enabled
    if (!config.get_settings().silent) {

      // Update progress
      float progress{100 * static_cast<float>(i) / static_cast<float>(config.get_params().max_steps - 1)};
      bar.set_progress(static_cast<std::size_t>(progress));
    }

    // Run averaging
    for (unsigned int j = 0; j < config.get_params().average; ++j) {
      config.update_params(i);
      boundary_condition->run();
      model.run();
      exporter.save(config.get_params());
    }
  }

  // Write data to disk
  exporter.flush();

  return 0;
}
