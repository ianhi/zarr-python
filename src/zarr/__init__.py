from zarr._version import version as __version__
from zarr.api.synchronous import (
    array,
    consolidate_metadata,
    copy,
    copy_all,
    copy_store,
    create,
    create_array,
    create_group,
    create_hierarchy,
    empty,
    empty_like,
    full,
    full_like,
    group,
    load,
    ones,
    ones_like,
    open,
    open_array,
    open_consolidated,
    open_group,
    open_like,
    save,
    save_array,
    save_group,
    tree,
    zeros,
    zeros_like,
)
from zarr.core.array import Array, AsyncArray
from zarr.core.config import config
from zarr.core.group import AsyncGroup, Group

# in case setuptools scm screw up and find version to be 0.0.0
assert not __version__.startswith("0.0.0")


def print_debug_info() -> None:
    """
    Print version info for use in bug reports.
    """
    import platform
    from importlib import import_module

    print(f"platform: {platform.platform()}")
    print(f"python: {platform.python_version()}\n")

    print(f"zarr: {__version__}\n")
    for package in ["numcodecs", "numpy", "fsspec", "s3fs", "botocore", "gcsfs"]:
        try:
            print(f"{package}: {import_module(package).__version__}")
        except ModuleNotFoundError:
            continue


__all__ = [
    "Array",
    "AsyncArray",
    "AsyncGroup",
    "Group",
    "__version__",
    "array",
    "config",
    "consolidate_metadata",
    "copy",
    "copy_all",
    "copy_store",
    "create",
    "create_array",
    "create_group",
    "create_hierarchy",
    "empty",
    "empty_like",
    "full",
    "full_like",
    "group",
    "load",
    "ones",
    "ones_like",
    "open",
    "open_array",
    "open_consolidated",
    "open_group",
    "open_like",
    "print_debug_info",
    "save",
    "save_array",
    "save_group",
    "tree",
    "zeros",
    "zeros_like",
]
