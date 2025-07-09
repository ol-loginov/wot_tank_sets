import collections
import copy

import ResMgr

import json


def del_key(ob, key):
    if key in ob: del ob[key]


def load_json_file(path):
    with open(path, 'rb') as f_in:
        return json.load(f_in, encoding='utf-8')


def vfs_directory_list(vfs_path):
    """Lists files in directory from VFS
    vfs_path: path in VFS, for example, 'scripts/client/gui/mods/'
    """
    result = []
    folder = ResMgr.openSection(vfs_path)
    if folder is not None and ResMgr.isDir(vfs_path):
        for name in folder.keys():
            if name not in result:
                result.append(name)
    ResMgr.purge(vfs_path, True)
    return sorted(result)


def vfs_file_read(vfs_path, as_binary=True):
    """Reads file from VFS
    vfs_path: path in VFS, for example, 'scripts/client/gui/mods/mod_.pyc'
    as_binary: set to True if file is binary
    """
    result = None
    vfs_file = ResMgr.openSection(vfs_path)
    if vfs_file is not None and ResMgr.isFile(vfs_path):
        result = str(vfs_file.asString)
        if as_binary:
            result = str(vfs_file.asBinary)
    ResMgr.purge(vfs_path, True)
    return result


def deep_dict_merge(dct1, dct2, override=True):
    """
    :param dct1: First dict to merge
    :param dct2: Second dict to merge
    :param override: if same key exists in both dictionaries, should override? otherwise ignore. (default=True)
    :return: The merge dictionary
    """
    merged = copy.deepcopy(dct1)
    for k, v2 in dct2.items():
        if k in merged:
            v1 = merged[k]
            if isinstance(v1, dict) and isinstance(v2, collections.Mapping):
                merged[k] = deep_dict_merge(v1, v2, override)
            elif isinstance(v1, list) and isinstance(v2, list):
                merged[k] = v1 + v2
            else:
                if override:
                    merged[k] = copy.deepcopy(v2)
        else:
            merged[k] = copy.deepcopy(v2)
    return merged
