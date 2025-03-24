from __future__ import annotations

import os
import re
import sys
from typing import TYPE_CHECKING, Any, get_args

import zarr
from zarr.core.config import config

from .conftest import zdtype_examples

if TYPE_CHECKING:
    from collections.abc import Generator

    from zarr.core.common import ZarrFormat
    from zarr.core.dtype.wrapper import _BaseDType, _BaseScalar

import numpy as np
import pytest

from zarr.core.dtype import (
    DTYPE,
    VariableLengthString,
    ZDType,
    data_type_registry,
    get_data_type_from_json,
)
from zarr.core.dtype._numpy import (
    Bool,
    Complex64,
    Complex128,
    DateTime64,
    FixedLengthAscii,
    FixedLengthBytes,
    FixedLengthUnicode,
    Float16,
    Float32,
    Float64,
    Int8,
    Int16,
    Int32,
    Int64,
    Structured,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
)
from zarr.core.dtype.common import DataTypeValidationError
from zarr.core.dtype.registry import DataTypeRegistry


@pytest.fixture
def data_type_registry_fixture() -> DataTypeRegistry:
    return DataTypeRegistry()


_NUMPY_SUPPORTS_VLEN_STRING = hasattr(np.dtypes, "StringDType")
VLEN_STRING_DTYPE: np.dtypes.StringDType | np.dtypes.ObjectDType
if _NUMPY_SUPPORTS_VLEN_STRING:
    VLEN_STRING_DTYPE = np.dtypes.StringDType()
    VLEN_STRING_CODE = "T"
else:
    VLEN_STRING_DTYPE = np.dtypes.ObjectDType()
    VLEN_STRING_CODE = "O"


def test_zdtype_examples() -> None:
    """
    Test that all the elements of the exported union type DTYPE have an example in the variable
    zdtype_examples, which we use for testing.

    If this test fails, that means that either there is a data type that does not have an example,
    or there is a data type that is missing from the DTYPE union type.
    """
    assert set(map(type, zdtype_examples)) == set(get_args(DTYPE))


@pytest.mark.parametrize(
    ("wrapper_cls", "np_dtype"),
    [
        (Bool, "bool"),
        (Int8, "int8"),
        (Int16, "int16"),
        (Int32, "int32"),
        (Int64, "int64"),
        (UInt8, "uint8"),
        (UInt16, "uint16"),
        (UInt32, "uint32"),
        (UInt64, "uint64"),
        (Float32, "float32"),
        (Float64, "float64"),
        (Complex64, "complex64"),
        (Complex128, "complex128"),
        (FixedLengthUnicode, "U"),
        (FixedLengthAscii, "S"),
        (FixedLengthBytes, "V"),
        (VariableLengthString, VLEN_STRING_CODE),
        (Structured, np.dtype([("a", np.float64), ("b", np.int8)])),
        (DateTime64, "datetime64[s]"),
    ],
)
def test_wrap(wrapper_cls: type[ZDType[Any, Any]], np_dtype: np.dtype[np.generic] | str) -> None:
    """
    Test that the wrapper class has the correct dtype class bound to the dtype_cls variable
    Test that the ``wrap`` method produces an instance of the wrapper class
    Test that the ``unwrap`` method returns the original dtype
    """
    dt = np.dtype(np_dtype)
    assert wrapper_cls.dtype_cls is type(dt)
    wrapped = wrapper_cls.from_dtype(dt)

    with pytest.raises(DataTypeValidationError, match="Invalid dtype"):
        wrapper_cls.from_dtype("not a dtype")  # type: ignore[arg-type]
    assert isinstance(wrapped, wrapper_cls)
    assert wrapped.to_dtype() == dt


@pytest.mark.parametrize("zdtype", zdtype_examples)
def test_to_json_roundtrip(zdtype: ZDType[Any, Any], zarr_format: ZarrFormat) -> None:
    """
    Test that a zdtype instance can round-trip through its JSON form
    """
    as_dict = zdtype.to_json(zarr_format=zarr_format)
    assert zdtype.from_json(as_dict, zarr_format=zarr_format) == zdtype


@pytest.mark.parametrize(
    ("wrapper", "expected_default"),
    [
        (Bool(), np.False_),
        (Int8(), np.int8(0)),
        (UInt8(), np.uint8(0)),
        (Int16(), np.int16(0)),
        (UInt16(), np.uint16(0)),
        (Int32(), np.int32(0)),
        (UInt32(), np.uint32(0)),
        (Int64(), np.int64(0)),
        (UInt64(), np.uint64(0)),
        (Float16(), np.float16(0)),
        (Float32(), np.float32(0)),
        (Float64(), np.float64(0)),
        (Complex64(), np.complex64(0)),
        (Complex128(), np.complex128(0)),
        (FixedLengthAscii(length=3), np.bytes_(b"")),
        (FixedLengthBytes(length=3), np.void(b"\x00\x00\x00")),
        (FixedLengthUnicode(length=3), np.str_("")),
        (
            Structured(fields=(("a", Float64()), ("b", Int8()))),
            np.array([0], dtype=[("a", np.float64), ("b", np.int8)])[0],
        ),
        (VariableLengthString(), ""),
        (DateTime64(unit="s"), np.datetime64("NaT")),
    ],
)
def test_default_value(wrapper: ZDType[Any, Any], expected_default: Any) -> None:
    """
    Test that the default_value method is correctly set for each dtype wrapper.
    """
    if isinstance(wrapper, DateTime64):
        assert np.isnan(wrapper.default_value())
    else:
        assert wrapper.default_value() == expected_default


@pytest.mark.parametrize(
    ("wrapper", "input_value", "expected_json"),
    [
        (Bool(), np.bool_(True), True),
        (Int8(), np.int8(42), 42),
        (UInt8(), np.uint8(42), 42),
        (Int16(), np.int16(42), 42),
        (UInt16(), np.uint16(42), 42),
        (Int32(), np.int32(42), 42),
        (UInt32(), np.uint32(42), 42),
        (Int64(), np.int64(42), 42),
        (UInt64(), np.uint64(42), 42),
        (Float16(), np.float16(42.0), 42.0),
        (Float32(), np.float32(42.0), 42.0),
        (Float64(), np.float64(42.0), 42.0),
        (Complex64(), np.complex64(42.0 + 1.0j), (42.0, 1.0)),
        (Complex128(), np.complex128(42.0 + 1.0j), (42.0, 1.0)),
        (FixedLengthAscii(length=4), np.bytes_(b"test"), "dGVzdA=="),
        (FixedLengthBytes(length=4), np.void(b"test"), "dGVzdA=="),
        (FixedLengthUnicode(length=4), np.str_("test"), "test"),
        (VariableLengthString(), "test", "test"),
        (DateTime64(unit="s"), np.datetime64("2021-01-01T00:00:00", "s"), 1609459200),
    ],
)
def test_to_json_value_v2(
    wrapper: ZDType[_BaseDType, _BaseScalar], input_value: Any, expected_json: Any
) -> None:
    """
    Test the to_json_value method for each dtype wrapper for zarr v2
    """
    assert wrapper.to_json_value(input_value, zarr_format=2) == expected_json


# NOTE! This test is currently a direct copy of the v2 version. When or if we change JSON serialization
# in a v3-specific manner, this test must be changed.
# TODO: Apply zarr-v3-specific changes to this test as needed
@pytest.mark.parametrize(
    ("wrapper", "input_value", "expected_json"),
    [
        (Bool(), np.bool_(True), True),
        (Int8(), np.int8(42), 42),
        (UInt8(), np.uint8(42), 42),
        (Int16(), np.int16(42), 42),
        (UInt16(), np.uint16(42), 42),
        (Int32(), np.int32(42), 42),
        (UInt32(), np.uint32(42), 42),
        (Int64(), np.int64(42), 42),
        (UInt64(), np.uint64(42), 42),
        (Float16(), np.float16(42.0), 42.0),
        (Float32(), np.float32(42.0), 42.0),
        (Float64(), np.float64(42.0), 42.0),
        (Complex64(), np.complex64(42.0 + 1.0j), (42.0, 1.0)),
        (Complex128(), np.complex128(42.0 + 1.0j), (42.0, 1.0)),
        (FixedLengthAscii(length=4), np.bytes_(b"test"), "dGVzdA=="),
        (FixedLengthBytes(length=4), np.void(b"test"), "dGVzdA=="),
        (FixedLengthUnicode(length=4), np.str_("test"), "test"),
        (VariableLengthString(), "test", "test"),
        (DateTime64(unit="s"), np.datetime64("2021-01-01T00:00:00", "s"), 1609459200),
    ],
)
def test_to_json_value_v3(
    wrapper: ZDType[_BaseDType, _BaseScalar], input_value: Any, expected_json: Any
) -> None:
    """
    Test the to_json_value method for each dtype wrapper for zarr v3
    """
    assert wrapper.to_json_value(input_value, zarr_format=3) == expected_json


@pytest.mark.parametrize(
    ("wrapper", "json_value", "expected_value"),
    [
        (Bool(), True, np.bool_(True)),
        (Int8(), 42, np.int8(42)),
        (UInt8(), 42, np.uint8(42)),
        (Int16(), 42, np.int16(42)),
        (UInt16(), 42, np.uint16(42)),
        (Int32(), 42, np.int32(42)),
        (UInt32(), 42, np.uint32(42)),
        (Int64(), 42, np.int64(42)),
        (UInt64(), 42, np.uint64(42)),
        (Float16(), 42.0, np.float16(42.0)),
        (Float32(), 42.0, np.float32(42.0)),
        (Float64(), 42.0, np.float64(42.0)),
        (Complex64(), (42.0, 1.0), np.complex64(42.0 + 1.0j)),
        (Complex128(), (42.0, 1.0), np.complex128(42.0 + 1.0j)),
        (FixedLengthAscii(length=4), "dGVzdA==", np.bytes_(b"test")),
        (FixedLengthBytes(length=4), "dGVzdA==", np.void(b"test")),
        (FixedLengthUnicode(length=4), "test", np.str_("test")),
        (VariableLengthString(), "test", "test"),
        (DateTime64(unit="s"), 1609459200, np.datetime64("2021-01-01T00:00:00", "s")),
    ],
)
def test_from_json_value(
    wrapper: ZDType[_BaseDType, _BaseScalar], json_value: Any, expected_value: Any
) -> None:
    """
    Test the from_json_value method for each dtype wrapper.
    """
    assert wrapper.from_json_value(json_value, zarr_format=2) == expected_value


class TestRegistry:
    @staticmethod
    def test_register(data_type_registry_fixture: DataTypeRegistry) -> None:
        """
        Test that registering a dtype in a data type registry works.
        """
        data_type_registry_fixture.register(Bool._zarr_v3_name, Bool)
        assert data_type_registry_fixture.get(Bool._zarr_v3_name) == Bool
        assert isinstance(data_type_registry_fixture.match_dtype(np.dtype("bool")), Bool)

    @staticmethod
    def test_override(data_type_registry_fixture: DataTypeRegistry) -> None:
        """
        Test that registering a new dtype with the same name works (overriding the previous one).
        """
        data_type_registry_fixture.register(Bool._zarr_v3_name, Bool)

        class NewBool(Bool):
            def default_value(self) -> np.bool_:
                return np.True_

        data_type_registry_fixture.register(NewBool._zarr_v3_name, NewBool)
        assert isinstance(data_type_registry_fixture.match_dtype(np.dtype("bool")), NewBool)

    @staticmethod
    @pytest.mark.parametrize(
        ("wrapper_cls", "dtype_str"), [(Bool, "bool"), (FixedLengthUnicode, "|U4")]
    )
    def test_match_dtype(
        data_type_registry_fixture: DataTypeRegistry,
        wrapper_cls: type[ZDType[_BaseDType, _BaseScalar]],
        dtype_str: str,
    ) -> None:
        """
        Test that match_dtype resolves a numpy dtype into an instance of the correspond wrapper for that dtype.
        """
        data_type_registry_fixture.register(wrapper_cls._zarr_v3_name, wrapper_cls)
        assert isinstance(data_type_registry_fixture.match_dtype(np.dtype(dtype_str)), wrapper_cls)

    @staticmethod
    def test_unregistered_dtype(data_type_registry_fixture: DataTypeRegistry) -> None:
        """
        Test that match_dtype raises an error if the dtype is not registered.
        """
        outside_dtype = "int8"
        with pytest.raises(
            ValueError, match=f"No data type wrapper found that matches dtype '{outside_dtype}'"
        ):
            data_type_registry_fixture.match_dtype(np.dtype(outside_dtype))

        with pytest.raises(KeyError):
            data_type_registry_fixture.get(outside_dtype)

    @staticmethod
    @pytest.mark.parametrize("zdtype", zdtype_examples)
    def test_registered_dtypes(
        zdtype: ZDType[_BaseDType, _BaseScalar], zarr_format: ZarrFormat
    ) -> None:
        """
        Test that the registered dtypes can be retrieved from the registry.
        """

        assert data_type_registry.match_dtype(zdtype.to_dtype()) == zdtype
        assert (
            data_type_registry.match_json(
                zdtype.to_json(zarr_format=zarr_format), zarr_format=zarr_format
            )
            == zdtype
        )

    @staticmethod
    @pytest.mark.parametrize("zdtype", zdtype_examples)
    def test_match_dtype_unique(
        zdtype: ZDType[Any, Any],
        data_type_registry_fixture: DataTypeRegistry,
        zarr_format: ZarrFormat,
    ) -> None:
        """
        Test that the match_dtype method uniquely specifies a registered data type. We create a local registry
        that excludes the data type class being tested, and ensure that an instance of the wrapped data type
        fails to match anything in the registry
        """
        for _cls in get_args(DTYPE):
            if _cls is not type(zdtype):
                data_type_registry_fixture.register(_cls._zarr_v3_name, _cls)

        dtype_instance = zdtype.to_dtype()

        msg = f"No data type wrapper found that matches dtype '{dtype_instance}'"
        with pytest.raises(ValueError, match=re.escape(msg)):
            data_type_registry_fixture.match_dtype(dtype_instance)

        instance_dict = zdtype.to_json(zarr_format=zarr_format)
        msg = f"No data type wrapper found that matches {instance_dict}"
        with pytest.raises(ValueError, match=re.escape(msg)):
            data_type_registry_fixture.match_json(instance_dict, zarr_format=zarr_format)


# this is copied from the registry tests -- we should deduplicate
here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def set_path() -> Generator[None, None, None]:
    sys.path.append(here)
    zarr.registry._collect_entrypoints()
    yield
    sys.path.remove(here)
    registries = zarr.registry._collect_entrypoints()
    for registry in registries:
        registry.lazy_load_list.clear()
    config.reset()


@pytest.mark.usefixtures("set_path")
def test_entrypoint_codec(zarr_format: ZarrFormat) -> None:
    from package_with_entrypoint import TestDataType

    instance = TestDataType()
    dtype_json = instance.to_json(zarr_format=zarr_format)
    assert get_data_type_from_json(dtype_json, zarr_format=zarr_format) == instance
