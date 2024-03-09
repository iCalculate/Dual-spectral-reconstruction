#pragma once

#include <h5pp/h5pp.h>
#include "ConfigParser.h"
#include "../event/EventStorage.h"

namespace snspd::io {
  class Exporter {
    ConfigParser &m_config;

    event::EventStorage &m_storage;

    std::vector<double>
        m_v,
        m_ib,
        m_t;

    h5pp::File m_file;

  public:

    explicit Exporter(ConfigParser &config, event::EventStorage &storage):
        m_config(config),
        m_storage(storage),
        m_v(config.get_params().max_steps, 0.0),
        m_ib(config.get_params().max_steps, 0.0),
        m_t(config.get_params().max_steps, 0.0),
        m_file(config.get_settings().output) {

      save(config.get_params());
    }

    void save(const Parameters &param);
    void flush();
  };
}


