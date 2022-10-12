from enum import Enum
from typing import List, Optional, Tuple, Union

from torch._C import device, dtype, layout

from typing_extensions import Literal

# defined in torch/csrc/profiler/python/init.cpp

class RecordScope(Enum):
    FUNCTION = ...
    BACKWARD_FUNCTION = ...
    TORCHSCRIPT_FUNCTION = ...
    KERNEL_FUNCTION_DTYPE = ...
    CUSTOM_CLASS = ...
    BUILD_FEATURE = ...
    LITE_INTERPRETER = ...
    USER_SCOPE = ...
    STATIC_RUNTIME_OP = ...
    STATIC_RUNTIME_MODEL = ...

class ProfilerState(Enum):
    Disable = ...
    CPU = ...
    CUDA = ...
    NVTX = ...
    ITT = ...
    KINETO = ...
    KINETO_GPU_FALLBACK = ...

class ActiveProfilerType(Enum):
    NONE = ...
    LEGACY = ...
    KINETO = ...
    NVTX = ...
    ITT = ...

class ProfilerActivity(Enum):
    CPU = ...
    CUDA = ...

class _EventType(Enum):
    TorchOp = ...
    Backend = ...
    Allocation = ...
    OutOfMemory = ...
    PyCall = ...
    PyCCall = ...
    Kineto = ...

class _ExperimentalConfig:
    def __init__(
        self,
        profiler_metrics: List[str] = ...,
        profiler_measure_per_kernel: bool = ...,
        verbose: bool = ...,
    ) -> None: ...
    ...

class ProfilerConfig:
    def __init__(
        self,
        state: ProfilerState,
        report_input_shapes: bool,
        profile_memory: bool,
        with_stack: bool,
        with_flops: bool,
        with_modules: bool,
        experimental_config: _ExperimentalConfig,
    ) -> None: ...
    ...

class _ProfilerEvent:
    start_tid: int
    start_time_ns: int
    children: List[_ProfilerEvent]

    # TODO(robieta): remove in favor of `self.typed`
    extra_fields: Union[
        _ExtraFields_TorchOp,
        _ExtraFields_Backend,
        _ExtraFields_Allocation,
        _ExtraFields_OutOfMemory,
        _ExtraFields_PyCall,
        _ExtraFields_PyCCall,
        _ExtraFields_Kineto,
    ]

    @property
    def typed(
        self,
    ) -> Union[
        Tuple[Literal[_EventType.TorchOp], _ExtraFields_TorchOp],
        Tuple[Literal[_EventType.Backend], _ExtraFields_Backend],
        Tuple[Literal[_EventType.Allocation], _ExtraFields_Allocation],
        Tuple[Literal[_EventType.OutOfMemory], _ExtraFields_OutOfMemory],
        Tuple[Literal[_EventType.PyCall], _ExtraFields_PyCall],
        Tuple[Literal[_EventType.PyCCall], _ExtraFields_PyCCall],
        Tuple[Literal[_EventType.Kineto], _ExtraFields_Kineto],
    ]: ...
    @property
    def name(self) -> str: ...
    @property
    def tag(self) -> _EventType: ...
    @property
    def id(self) -> int: ...
    @property
    def parent(self) -> Optional[_ProfilerEvent]: ...
    @property
    def correlation_id(self) -> int: ...
    @property
    def end_time_ns(self) -> int: ...
    @property
    def duration_time_ns(self) -> int: ...

class _Inputs:
    shapes: List[List[int]]
    dtypes: List[str]
    strides: List[List[int]]
    ivalues: List[Union[int, float, bool, complex]]
    tensor_metadata: List[Optional[_TensorMetadata]]

class _TensorMetadata:
    impl_ptr: Optional[int]
    storage_data_ptr: Optional[int]
    id: Optional[int]

    @property
    def layout(self) -> layout: ...
    @property
    def device(self) -> device: ...
    @property
    def dtype(self) -> dtype: ...

class _ExtraFields_TorchOp:
    inputs: _Inputs
    sequence_number: int
    allow_tf32_cublas: bool

    @property
    def scope(self) -> RecordScope: ...

class _ExtraFields_Backend: ...

class _ExtraFields_Allocation:
    ptr: int
    id: Optional[int]
    alloc_size: int
    total_allocated: int
    total_reserved: int

    @property
    def device(self) -> device: ...

class _ExtraFields_OutOfMemory: ...

class _PyFrameState:
    line_number: int
    function_name: str

    @property
    def file_name(self) -> str: ...

class _NNModuleInfo:
    @property
    def params(self) -> List[Tuple[str, int]]: ...
    @property
    def self_ptr(self) -> int: ...
    @property
    def cls_ptr(self) -> int: ...
    @property
    def cls_name(self) -> str: ...

class _OptimizerInfo:
    @property
    def parameters(
        self,
    ) -> List[
        Tuple[
            # Parameter
            _TensorMetadata,
            #
            # Gradient (if present during optimizer.step())
            Optional[_TensorMetadata],
            #
            # Optimizer state for Parameter as (name, tensor) pairs
            List[Tuple[str, _TensorMetadata]],
        ]
    ]: ...

class _ExtraFields_PyCCall:
    @property
    def callsite(self) -> _PyFrameState: ...
    @property
    def caller(self) -> _PyFrameState: ...
    @property
    def module(self) -> Optional[_NNModuleInfo]: ...
    @property
    def optimizer(self) -> Optional[_OptimizerInfo]: ...

class _ExtraFields_PyCall:
    caller: _PyFrameState

class _ExtraFields_Kineto: ...
