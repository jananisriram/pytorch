#pragma once

#include <c10/macros/Export.h>
#include <chrono>
#include <condition_variable>
#include <mutex>
#include <thread>
#include <vector>
#include <future>

namespace c10d {

class TORCH_API Healthcheck {
 public:
    Healthcheck(
        bool abortOnError = false,
        std::chrono::milliseconds interval = std::chrono::seconds(10),
        std::chrono::milliseconds timeout = std::chrono::seconds(10)
    );
  virtual ~Healthcheck();

  void shutdown();
 private:
  // Called to setup each side, this is run on the worker thread.
  virtual void setup(int side) = 0;

  // Called in an individual thread to run the healthcheck.
  virtual void runHealthcheck(int side) = 0;

  void runLoop();

 private:
  bool abortOnError_;
  std::chrono::milliseconds interval_;
  std::chrono::milliseconds timeout_;

  std::future<void> worker_{};

  std::mutex shutdownM_;
  std::condition_variable shutdownCv_;
  bool shutdown_{false};
};

}
