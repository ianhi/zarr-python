"""
Public type definitions for Zarr.

This module defines commonly used type aliases and literals that appear in Zarr's API.
These types are defined here to enable proper cross-referencing in the documentation
without creating circular imports.
"""

from __future__ import annotations

import sys
from collections.abc import Iterable, Mapping, Sequence
from os import PathLike
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union

if sys.version_info >= (3, 11):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

# Import numpy types
if TYPE_CHECKING:
    import numpy as np
    import numpy.typing as npt

# Core type aliases - always available at runtime for documentation
ZarrFormat: TypeAlias = Literal[2, 3]
"""Zarr format version. Can be either 2 or 3."""

MemoryOrder: TypeAlias = Literal["C", "F"]
"""Memory layout order. Can be either 'C' (row-major) or 'F' (column-major)."""

NodeType: TypeAlias = Literal["array", "group"]
"""Type of Zarr node. Can be either 'array' or 'group'."""

AccessModeLiteral: TypeAlias = Literal["r", "r+", "a", "w", "w-"]
"""File access mode. Can be 'r', 'r+', 'a', 'w', or 'w-'."""

JSON: TypeAlias = None | bool | int | float | str | list["JSON"] | dict[str, "JSON"]
"""JSON-serializable data type."""

BytesLike: TypeAlias = bytes | bytearray | memoryview
"""Bytes-like object. Can be bytes, bytearray, or memoryview."""

ChunkCoords: TypeAlias = tuple[int, ...]
"""Chunk coordinates as a tuple of integers."""

ChunkCoordsLike: TypeAlias = Iterable[int]
"""Chunk coordinates specification. Any iterable of integers."""

ShapeLike: TypeAlias = int | ChunkCoords
"""Array shape specification. Can be a tuple of integers or a single integer."""

DimensionNames: TypeAlias = Iterable[str] | None
"""Dimension names specification. Can be an iterable of strings or None."""

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

# Type variables for generics
T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)

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
    Array: TypeAlias = "zarr.core.array.Array[Any]"
    AsyncArray: TypeAlias = "zarr.core.array.AsyncArray[Any]"
    Group: TypeAlias = "zarr.core.group.Group"
    AsyncGroup: TypeAlias = "zarr.core.group.AsyncGroup"
    DefaultFillValue: TypeAlias = "zarr.core.common.DefaultFillValue"
    ZDType: TypeAlias = "zarr.core.dtype.ZDType"
"""Core Zarr classes."""

# Store types with forward references
if TYPE_CHECKING:
    from zarr.abc.store import Store as _Store
    from zarr.storage import StorePath as _StorePath

    Store: TypeAlias = _Store
    StorePath: TypeAlias = _StorePath
else:
    Store = TypeVar("Store")
    StorePath = TypeVar("StorePath")

StoreLike: TypeAlias = Union[Store, StorePath, PathLike[str], str, dict[str, Any], Mapping[str, Any]]
"""Store-like object. Can be a Store, StorePath, Path, str, or dict."""

# Array types with proper numpy typing
if TYPE_CHECKING:
    NDArrayLike: TypeAlias = npt.NDArray[Any] | np.generic
else:
    NDArrayLike: TypeAlias = "numpy.ndarray[Any, Any] | numpy.generic"
"""N-dimensional array-like object."""

NDArrayLikeOrScalar: TypeAlias = Union[NDArrayLike, Any]
"""N-dimensional array-like object or scalar value."""

ArrayLike: TypeAlias = Union[Sequence[Any], NDArrayLike]
"""Array-like object."""

# ZDType - special handling for strong typing
if TYPE_CHECKING:
    from zarr.core.dtype import ZDType as _ZDTypeRuntime

    ZDTypeLike: TypeAlias = _ZDTypeRuntime | Any
else:
    # At runtime, use forward reference
    ZDTypeLike: TypeAlias = "zarr.core.dtype.ZDType | typing.Any"
"""Zarr data type specification."""

# Metadata types
ArrayMetadata: TypeAlias = Any
"""Array metadata."""

ArrayMetadataDict: TypeAlias = dict[str, JSON]
"""Array metadata as a dictionary."""

ArrayV2MetadataDict: TypeAlias = dict[str, JSON]
"""Array V2 metadata as a dictionary."""

ArrayV3MetadataDict: TypeAlias = dict[str, JSON]
"""Array V3 metadata as a dictionary."""

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
    ArrayV2Metadata: TypeAlias = "zarr.core.array_spec.ArrayV2Metadata"
    ArrayV3Metadata: TypeAlias = "zarr.core.array_spec.ArrayV3Metadata"
    GroupMetadata: TypeAlias = "zarr.core.group.GroupMetadata"
    ConsolidatedMetadata: TypeAlias = "zarr.core.group.ConsolidatedMetadata"
"""Metadata classes."""

# Codec types with proper forward references
if TYPE_CHECKING:
    from zarr.abc.codec import BytesBytesCodec as _BytesBytesCodec

    CompressorLike: TypeAlias = dict[str, JSON] | _BytesBytesCodec | Any | Literal["auto"] | None
else:
    CompressorLike: TypeAlias = Union[
        dict[str, JSON],
        "zarr.abc.codec.BytesBytesCodec",
        Any,
        Literal["auto"],
        None,
    ]
"""Compressor specification."""

CompressorsLike: TypeAlias = Iterable[CompressorLike]
"""Compressors specification."""

FiltersLike: TypeAlias = Iterable[Any]
"""Filters specification."""

SerializerLike: TypeAlias = Any
"""Serializer specification."""

ShardsLike: TypeAlias = tuple[int, ...] | None
"""Shards specification."""

CompressorLikev2: TypeAlias = dict[str, JSON] | Any | None
"""Compressor specification for Zarr v2."""

# Chunk key encoding types
if TYPE_CHECKING:
    from zarr.core.chunk_key_encodings import ChunkKeyEncoding as _ChunkKeyEncoding
    from zarr.core.chunk_key_encodings import ChunkKeyEncodingParams as _ChunkKeyEncodingParams

    ChunkKeyEncodingLike: TypeAlias = _ChunkKeyEncodingParams | _ChunkKeyEncoding
    ChunkKeyEncoding: TypeAlias = _ChunkKeyEncoding
    ChunkKeyEncodingParams: TypeAlias = _ChunkKeyEncodingParams
else:
    ChunkKeyEncodingLike: TypeAlias = Union[
        "zarr.core.chunk_key_encodings.ChunkKeyEncodingParams",
        "zarr.core.chunk_key_encodings.ChunkKeyEncoding",
    ]
    ChunkKeyEncoding: TypeAlias = "zarr.core.chunk_key_encodings.ChunkKeyEncoding"
    ChunkKeyEncodingParams: TypeAlias = "zarr.core.chunk_key_encodings.ChunkKeyEncodingParams"
"""Chunk key encoding specification."""

# Array config types
if TYPE_CHECKING:
    from zarr.core.array_spec import ArrayConfig as _ArrayConfig
    from zarr.core.array_spec import ArrayConfigLike as _ArrayConfigLike

    ArrayConfig: TypeAlias = _ArrayConfig
    ArrayConfigLike: TypeAlias = _ArrayConfigLike
else:
    # Import at runtime for autoapi to resolve
    try:
        from zarr.core.array_spec import ArrayConfig, ArrayConfigLike
    except ImportError:
        ArrayConfig = TypeVar("ArrayConfig")
        ArrayConfigLike = TypeVar("ArrayConfigLike")
"""Array configuration specification."""

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
    # Import at runtime for autoapi to resolve
    try:
        from zarr.abc.codec import BaseCodec, ArrayArrayCodec, ArrayBytesCodec, BytesBytesCodec, CodecPipeline
        Codec = BaseCodec  # Alias to the imported class
    except ImportError:
        BaseCodec = TypeVar("BaseCodec")
        ArrayArrayCodec = TypeVar("ArrayArrayCodec")
        ArrayBytesCodec = TypeVar("ArrayBytesCodec")
        BytesBytesCodec = TypeVar("BytesBytesCodec")
        CodecPipeline = TypeVar("CodecPipeline")
        Codec = BaseCodec  # Alias to the TypeVar
"""Codec types for data transformation."""

# Store protocols
if TYPE_CHECKING:
    from zarr.abc.store import ByteGetter as _ByteGetter
    from zarr.abc.store import ByteSetter as _ByteSetter

    ByteGetter: TypeAlias = _ByteGetter
    ByteSetter: TypeAlias = _ByteSetter
else:
    ByteGetter: TypeAlias = "zarr.abc.store.ByteGetter"
    ByteSetter: TypeAlias = "zarr.abc.store.ByteSetter"
"""Store byte access protocols."""


# Store request types - define as classes for better documentation
class RangeByteRequest:
    """Request a specific byte range."""

    start: int
    end: int


class OffsetByteRequest:
    """Request all bytes starting from a given byte offset."""

    offset: int


class SuffixByteRequest:
    """Request up to the last `n` bytes."""

    suffix: int


ByteRequest: TypeAlias = Union[RangeByteRequest, OffsetByteRequest, SuffixByteRequest]
"""Byte range request."""

__all__ = [
    # Core type aliases
    "ZarrFormat",
    "MemoryOrder",
    "NodeType",
    "AccessModeLiteral",
    "JSON",
    "BytesLike",
    "ShapeLike",
    "ChunkCoords",
    "ChunkCoordsLike",
    "DimensionNames",
    # Core classes
    "Array",
    "AsyncArray",
    "Group",
    "AsyncGroup",
    "DefaultFillValue",
    "ZDType",
    # Store types
    "Store",
    "StorePath",
    "StoreLike",
    "ByteRequest",
    "RangeByteRequest",
    "OffsetByteRequest",
    "SuffixByteRequest",
    "ByteGetter",
    "ByteSetter",
    # Buffer types
    "ArrayLike",
    "NDArrayLike",
    "NDArrayLikeOrScalar",
    # Metadata types
    "ArrayMetadata",
    "ArrayMetadataDict",
    "ArrayV2MetadataDict",
    "ArrayV3MetadataDict",
    "ArrayV2Metadata",
    "ArrayV3Metadata",
    "GroupMetadata",
    "ConsolidatedMetadata",
    "CompressorLikev2",
    # Chunk key encoding and array config
    "ChunkKeyEncoding",
    "ChunkKeyEncodingParams",
    "ChunkKeyEncodingLike",
    "ArrayConfig",
    "ArrayConfigLike",
    # Data type related
    "ZDTypeLike",
    # Array and codec types
    "CompressorLike",
    "CompressorsLike",
    "FiltersLike",
    "SerializerLike",
    "ShardsLike",
    # Enums
    "BloscCname",
    "BloscShuffle",
    "Endian",
    "ShardingCodecIndexLocation",
    "Order",
    # Codec types
    "BaseCodec",
    "ArrayArrayCodec",
    "ArrayBytesCodec",
    "BytesBytesCodec",
    "CodecPipeline",
    "Codec",
]

