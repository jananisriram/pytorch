#pragma once

#include <c10/macros/Export.h>
#include <c10/cuda/CUDAStream.h>
#include <torch/csrc/distributed/c10d/Healthcheck.hpp>
#include <torch/csrc/distributed/c10d/ProcessGroupNCCL.hpp>
#include <torch/csrc/distributed/c10d/Store.hpp>

namespace c10d {

class TORCH_API HealthcheckNCCL : public Healthcheck {
  public:
    HealthcheckNCCL(
      const c10::intrusive_ptr<Store>& store,
        int rank,
        int worldSize,
        bool abortOnError = false,
        std::chrono::milliseconds interval = std::chrono::seconds(10),
        std::chrono::milliseconds timeout = std::chrono::seconds(10)
    );
    ~HealthcheckNCCL() override;

  protected:
    void setup(int side) override;
    void runHealthcheck(int side) override;

  private:
    int rank_;
    int worldSize_;
    const c10::intrusive_ptr<Store> store_;
    std::vector<at::cuda::CUDAStream> streams_;
    std::vector<ProcessGroupNCCL> processGroups_;
};

}
