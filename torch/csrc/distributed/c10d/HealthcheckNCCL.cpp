#include <torch/csrc/distributed/c10d/HealthcheckNCCL.hpp>

#include <fmt/format.h>

#include <c10/cuda/CUDAStream.h>
#include <c10/util/intrusive_ptr.h>
#include <torch/csrc/distributed/c10d/Healthcheck.hpp>
#include <torch/csrc/distributed/c10d/PrefixStore.hpp>

namespace c10d {

HealthcheckNCCL::HealthcheckNCCL(
    const c10::intrusive_ptr<::c10d::Store>& store,
    int rank,
    int worldSize,
    bool abortOnError,
    std::chrono::milliseconds interval,
    std::chrono::milliseconds timeout) : Healthcheck(abortOnError, interval, timeout), rank_(rank), worldSize_(worldSize) {
    streams_.reserve(2);
    processGroups_.reserve(2);
}

void HealthcheckNCCL::setup(int side) {
    // TODO: need to figure out how to always go cross host
    auto group = (rank_+side) % 2;
    auto store = c10::make_intrusive<PrefixStore>(fmt::format("/healthcheck/{}", group), store_);
    streams_.emplace_back();
    processGroups_.emplace_back(
        store,
        rank_ % 2,
        2,
    );
}

void HealthcheckNCCL::runHealthcheck(int side) {
    at::cuda::setCurrentCUDAStream(streams_.at(side));
    auto& pg = processGroups_.at(side);

    // TODO fix + device
    auto out = pg.allreduce(at::ones({1.0}, at::kFloat32), {});
}


}
