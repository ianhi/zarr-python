"""Public type definitions and constants"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from os import PathLike
from typing import TYPE_CHECKING, Any, Literal, TypeAlias, TypeVar

# Import core types from zarr.core.types
from zarr.core.types import (
    JSON,
    AccessModeLiteral,
    ArrayMetadataJSON_V2,
    ArrayMetadataJSON_V3,
    BytesLike,
    ChunkCoords,
    ChunkCoordsLike,
    DimensionNames,
    GroupMetadataJSON_V2,
    GroupMetadataJSON_V3,
    MemoryOrder,
    NodeType,
    ShapeLike,
    ZarrFormat,
)

# Additional types needed for comprehensive documentation linking
# These extend the minimal set from zarr.core.types

# Import numpy types for proper typing
if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt

# Core classes - forward references for main API classes
if TYPE_CHECKING:
    from zarr.core.array import Array as _Array
    from zarr.core.array import AsyncArray as _AsyncArray
    from zarr.core.common import DefaultFillValue as _DefaultFillValue
    from zarr.core.dtype import ZDType as _ZDType
    from zarr.core.group import AsyncGroup as _AsyncGroup
    from zarr.core.group import Group as _Group

    Array: TypeAlias = _Array[Any]
    AsyncArray: TypeAlias = _AsyncArray[Any]
    Group: TypeAlias = _Group
    AsyncGroup: TypeAlias = _AsyncGroup
    DefaultFillValue: TypeAlias = _DefaultFillValue
    ZDType: TypeAlias = _ZDType
else:
    # Import at runtime for autoapi to resolve
    try:
        from zarr.core.array import Array, AsyncArray
        from zarr.core.common import DefaultFillValue
        from zarr.core.dtype import ZDType
        from zarr.core.group import AsyncGroup, Group
    except ImportError:
        # Fallback to TypeVar placeholders
        Array = TypeVar("Array")
        AsyncArray = TypeVar("AsyncArray")
        Group = TypeVar("Group")
        AsyncGroup = TypeVar("AsyncGroup")
        DefaultFillValue = TypeVar("DefaultFillValue")
        ZDType = TypeVar("ZDType")

# Store types with forward references
if TYPE_CHECKING:
    from zarr.abc.store import Store as _Store
    from zarr.storage import StorePath as _StorePath

    Store: TypeAlias = _Store
    StorePath: TypeAlias = _StorePath
else:
    # Import at runtime for autoapi to resolve
    Store = TypeVar("Store")
    StorePath = TypeVar("StorePath")

StoreLike: TypeAlias = Store | StorePath | PathLike[str] | str | dict[str, Any] | Mapping[str, Any]
"""Store-like object. Can be a Store, StorePath, Path, str, or dict."""

# Array types with proper numpy typing
if TYPE_CHECKING:
    NDArrayLike: TypeAlias = npt.NDArray[Any] | np.generic
else:
    NDArrayLike = TypeVar("NDArrayLike")

NDArrayLikeOrScalar: TypeAlias = NDArrayLike | Any
ArrayLike: TypeAlias = Sequence[Any] | NDArrayLike

# ZDType - special handling for strong typing
if TYPE_CHECKING:
    from zarr.core.dtype import ZDType as _ZDTypeRuntime

    ZDTypeLike: TypeAlias = _ZDTypeRuntime | Any
else:
    ZDTypeLike = TypeVar("ZDTypeLike")

# Chunk key encoding types
if TYPE_CHECKING:
    from zarr.core.chunk_key_encodings import ChunkKeyEncoding as _ChunkKeyEncoding
    from zarr.core.chunk_key_encodings import ChunkKeyEncodingParams as _ChunkKeyEncodingParams

    ChunkKeyEncodingLike: TypeAlias = _ChunkKeyEncodingParams | _ChunkKeyEncoding
    ChunkKeyEncoding: TypeAlias = _ChunkKeyEncoding
    ChunkKeyEncodingParams: TypeAlias = _ChunkKeyEncodingParams
else:
    ChunkKeyEncodingLike = TypeVar("ChunkKeyEncodingLike")
    ChunkKeyEncoding = TypeVar("ChunkKeyEncoding")
    ChunkKeyEncodingParams = TypeVar("ChunkKeyEncodingParams")

# Array config types
if TYPE_CHECKING:
    from zarr.core.array_spec import ArrayConfig as _ArrayConfig
    from zarr.core.array_spec import ArrayConfigLike as _ArrayConfigLike

    ArrayConfig: TypeAlias = _ArrayConfig
    ArrayConfigLike: TypeAlias = _ArrayConfigLike
else:
    try:
        from zarr.core.array_spec import ArrayConfig, ArrayConfigLike
    except ImportError:
        ArrayConfig = TypeVar("ArrayConfig")
        ArrayConfigLike = TypeVar("ArrayConfigLike")

# Codec class types
if TYPE_CHECKING:
    from zarr.abc.codec import ArrayArrayCodec as _ArrayArrayCodec
    from zarr.abc.codec import ArrayBytesCodec as _ArrayBytesCodec
    from zarr.abc.codec import BaseCodec as _BaseCodec
    from zarr.abc.codec import BytesBytesCodec as _BytesBytesCodec
    from zarr.abc.codec import CodecPipeline as _CodecPipeline

    BaseCodec: TypeAlias = _BaseCodec[Any, Any]
    ArrayArrayCodec: TypeAlias = _ArrayArrayCodec[Any, Any]
    ArrayBytesCodec: TypeAlias = _ArrayBytesCodec[Any]
    BytesBytesCodec: TypeAlias = _BytesBytesCodec
    CodecPipeline: TypeAlias = _CodecPipeline[Any]
    Codec: TypeAlias = _BaseCodec[Any, Any]
else:
    try:
        from zarr.abc.codec import (
            ArrayArrayCodec,
            ArrayBytesCodec,
            BaseCodec,
            BytesBytesCodec,
            CodecPipeline,
        )

        Codec = BaseCodec
    except ImportError:
        BaseCodec = TypeVar("BaseCodec")
        ArrayArrayCodec = TypeVar("ArrayArrayCodec")
        ArrayBytesCodec = TypeVar("ArrayBytesCodec")
        BytesBytesCodec = TypeVar("BytesBytesCodec")
        CodecPipeline = TypeVar("CodecPipeline")
        Codec = BaseCodec

# Additional commonly used types
ArrayMetadata: TypeAlias = Any
ArrayMetadataDict: TypeAlias = dict[str, JSON]
ArrayV2MetadataDict: TypeAlias = dict[str, JSON]
ArrayV3MetadataDict: TypeAlias = dict[str, JSON]

# Additional metadata types with forward references
if TYPE_CHECKING:
    from zarr.core.array_spec import ArrayV2Metadata as _ArrayV2Metadata
    from zarr.core.array_spec import ArrayV3Metadata as _ArrayV3Metadata
    from zarr.core.group import ConsolidatedMetadata as _ConsolidatedMetadata
    from zarr.core.group import GroupMetadata as _GroupMetadata

    ArrayV2Metadata: TypeAlias = _ArrayV2Metadata
    ArrayV3Metadata: TypeAlias = _ArrayV3Metadata
    GroupMetadata: TypeAlias = _GroupMetadata
    ConsolidatedMetadata: TypeAlias = _ConsolidatedMetadata
else:
    GroupMetadata = TypeVar("GroupMetadata")
    ConsolidatedMetadata = TypeVar("ConsolidatedMetadata")

# Codec types
if TYPE_CHECKING:
    from zarr.abc.codec import BytesBytesCodec as _BytesBytesCodec

    CompressorLike: TypeAlias = dict[str, JSON] | _BytesBytesCodec | Any | Literal["auto"] | None
else:
    CompressorLike: TypeAlias = dict[str, JSON] | Any | Literal["auto"] | None

CompressorsLike: TypeAlias = Iterable[CompressorLike]
FiltersLike: TypeAlias = Iterable[Any]
SerializerLike: TypeAlias = Any
ShardsLike: TypeAlias = tuple[int, ...] | None
CompressorLikev2: TypeAlias = dict[str, JSON] | Any | None

# Store protocols
if TYPE_CHECKING:
    from zarr.abc.store import ByteGetter as _ByteGetter
    from zarr.abc.store import ByteSetter as _ByteSetter

    ByteGetter: TypeAlias = _ByteGetter
    ByteSetter: TypeAlias = _ByteSetter
else:
    ByteGetter = TypeVar("ByteGetter")
    ByteSetter = TypeVar("ByteSetter")

# Import enums at runtime - these don't cause circular imports
try:
    from zarr.codecs.blosc import BloscCname, BloscShuffle
    from zarr.codecs.bytes import Endian
    from zarr.codecs.sharding import ShardingCodecIndexLocation
    from zarr.core.indexing import Order
except ImportError:
    # Fallback if imports fail
    BloscCname = Any
    BloscShuffle = Any
    Endian = Any
    ShardingCodecIndexLocation = Any
    Order = Any

__all__ = [
    # Basic type aliases from zarr.core.types
    "JSON",
    "AccessModeLiteral",
    # Extended types for comprehensive documentation linking
    # Core classes
    "Array",
    "ArrayArrayCodec",
    "ArrayBytesCodec",
    # Array config
    "ArrayConfig",
    "ArrayConfigLike",
    # Array types
    "ArrayLike",
    # Metadata types
    "ArrayMetadata",
    "ArrayMetadataDict",
    # Core metadata types from zarr.core.types
    "ArrayMetadataJSON_V2",
    "ArrayMetadataJSON_V3",
    "ArrayV2Metadata",
    "ArrayV2MetadataDict",
    "ArrayV3Metadata",
    "ArrayV3MetadataDict",
    "AsyncArray",
    "AsyncGroup",
    # Codec types
    "BaseCodec",
    # Enums
    "BloscCname",
    "BloscShuffle",
    "ByteGetter",
    "ByteSetter",
    "BytesBytesCodec",
    "BytesLike",
    "ChunkCoords",
    "ChunkCoordsLike",
    # Chunk key encoding
    "ChunkKeyEncoding",
    "ChunkKeyEncodingLike",
    "ChunkKeyEncodingParams",
    "Codec",
    "CodecPipeline",
    "CompressorLike",
    "CompressorLikev2",
    "CompressorsLike",
    "ConsolidatedMetadata",
    "DefaultFillValue",
    "DimensionNames",
    "Endian",
    "FiltersLike",
    "Group",
    "GroupMetadata",
    "GroupMetadataJSON_V2",
    "GroupMetadataJSON_V3",
    "MemoryOrder",
    "NDArrayLike",
    "NDArrayLikeOrScalar",
    "NodeType",
    "Order",
    "SerializerLike",
    "ShapeLike",
    "ShardingCodecIndexLocation",
    "ShardsLike",
    # Store types
    "Store",
    "StoreLike",
    "StorePath",
    "ZDType",
    "ZDTypeLike",
    "ZarrFormat",
]

# Post-import patching for types that have circular import issues
if not TYPE_CHECKING:
    try:
        from zarr.storage._common import StorePath as _StorePath_Runtime

        StorePath = _StorePath_Runtime

        from zarr.abc.store import Store as _Store_Runtime

        Store = _Store_Runtime

        # Update StoreLike with the real types
        StoreLike = Store | StorePath | PathLike[str] | str | dict[str, Any] | Mapping[str, Any]
    except ImportError:
        pass  # Keep the TypeVar fallbacks
