#!/usr/bin/env python2.7

import os
import zipfile
from distutils.dir_util import copy_tree, remove_tree
from distutils import log
from py_compile import compile

# mod props
mod_author_id = 'com.github.ol_loginov'
mod_pack_id = 'wot_tank_filter'
mod_id = mod_author_id + '.' + mod_pack_id

# current folder
build_folder = os.path.dirname(os.path.abspath(__file__))

# sources & targets
src_folder = os.path.join(build_folder, 'src')
target_folder = os.path.join(build_folder, 'target')

# wotmod generation
wotmod_root = os.path.join(target_folder, 'wotmod')
wotmod_file = os.path.join(target_folder, '%s.wotmod' % (mod_id))


def panic(message):
    log.fatal(message)
    raise EnvironmentError(message)


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.isdir(path):
        panic('%s is not a folder' % path)


def create_wotmod():
    def walk_dir(path, zip_handle):
        """
        :param path: path to add
        :param zip_handle: zip file handle
        """
        for root, dirs, files in os.walk(path):
            for f in files:
                src = os.path.join(root, f)
                dst = os.path.relpath(os.path.join(root, f), path)
                zip_handle.write(src, dst)

    with zipfile.ZipFile(wotmod_file, mode='w', compression=zipfile.ZIP_STORED) as out_file:
        walk_dir(wotmod_root, out_file)


def compile_sources():
    for root, dirs, files in os.walk(wotmod_root):
        for f in files:
            src = os.path.join(root, f)
            if os.path.basename(src).endswith('.py'):
                compile(src, doraise=True)


def build():
    log.info('Remove target folder...')
    remove_tree(target_folder)

    if os.path.exists(target_folder):
        panic('Cannot cleanup target folder "%s"' % target_folder)

    log.info('Create target folder...')
    ensure_folder(wotmod_root)

    log.info('Copy sources...')
    copy_tree(src_folder, wotmod_root, verbose=False)

    log.info('Compile pythons...')
    compile_sources()

    log.info('Make wotmod archive...')
    create_wotmod()


log.set_threshold(log.INFO)
build()

log.info('Done! Result is in "%s"' % wotmod_file)
