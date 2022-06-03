import fcntl
import os
import struct

from middlewared.service import CallError
from enum import IntFlag


ZFS_IOC_GETDOSFLAGS = 0x80088301
ZFS_IOC_SETDOSFLAGS = 0x40088302


class DOSFlag(IntFlag):
    READONLY = 0x0000000100000000
    HIDDEN = 0x0000000200000000
    SYSTEM = 0x0000000400000000
    ARCHIVE = 0x0000000800000000
    REPARSE = 0x0000080000000000
    OFFLINE = 0x0000100000000000
    SPARSE = 0x0000200000000000
    ALL = 0x0000380f00000000


def get_dosflags(path: str) -> dict:
    fd = os.open(path, os.O_RDONLY)
    try:
        rv = get_dosflags_impl(path, fd)
        out = {}
        for f in DOSFlag:
            if f == DOSFlag.ALL:
                continue

            out[f.name.lower()] = True if rv & f else False

        return out
    finally:
        os.close(fd)


def get_dosflags_impl(path: str, fd: int) -> int:
    fl = struct.unpack('L', fcntl.ioctl(fd, ZFS_IOC_GETDOSFLAGS, struct.pack('L', 0)))
    if not fl:
        raise CallError(f'Unable to retrieve attribute of {path!r} path')
    return fl[0]


def set_dosflags(path: str, dosflags: dict) -> None:
    flags_in = 0
    for flag, enabled in dosflags.items():
        if not enabled:
            continue
        flags_in |= DOSFlag[flag.upper()]

    fd = os.open(path, os.O_RDONLY)
    try:
        current_flags = get_dosflags_impl(path, fd) & ~DOSFlag.ALL
        set_dosflags_impl(fd, path, flags_in | current_flags)
    finally:
        os.close(fd)


def set_dosflags_impl(fd: int, path: str, flags: int) -> None:
    fcntl.ioctl(fd, ZFS_IOC_SETDOSFLAGS, struct.pack('L', flags))
    if flags != get_dosflags_impl(path, fd):
        raise CallError(f'Unable to set dos flag at {path!r}')
