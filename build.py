#!/usr/bin/env python3

import argparse
from os import path
import os
import re
import sys
import time
from tempfile import gettempdir

import uflash
import python_minifier


def replace_includes(content: str, file_path: str) -> str:
    start_includes = re.search(r"# <Includes>", content, re.MULTILINE)
    end_includes = re.search(r"# </Includes>", content, re.MULTILINE)
    if start_includes:
        if not end_includes:
            raise ValueError(f"Parse error #</Includes> in {file_path}")
        start_includes_pos = start_includes.end()
        end_includes_pos = end_includes.start()
        includes = content[start_includes_pos:end_includes_pos - 1]
        resolved_content = resolves(includes.strip(), file_path)

        return "".join([content[0: start_includes_pos],
                        "\n",
                        resolved_content,
                        "\n",
                        content[end_includes_pos: len(content)]])
    else:
        return content


def resolve(include: str, file_path: str) -> str:
    matches = re.match(r"from (?P<package>[a-zA-Z0-9_\.]+) import (?P<module>([a-zA-Z0-9_\.]+|\*))", include)
    match_dict = matches.groupdict()
    package = match_dict['package'].strip()
    module = match_dict['module'].strip()
    if module != '*':
        raise ValueError(f"Only import * is supported in {file_path}. {include}")

    package_file_path = f"{package.replace('.', '/')}.py"

    try:
        with open(package_file_path, 'r') as file:
            read_data = file.read()
    except Exception as package_file_open_exception:
        raise ValueError(f"Unable to read file {package_file_path} in {file_path}. {include}") \
            from package_file_open_exception

    return replace_includes(read_data, package_file_path)


def resolves(includes: str, file_path: str) -> str:
    includes_array = includes.split("\n")
    resolved_content = []
    for include in includes_array:
        resolved_content.append(resolve(include, file_path))
    return "\n".join(resolved_content)


def flash(path_to_python: str, path_to_output: str, flash: bool):
    try:
        with open(path_to_python, 'r') as file:
            main_file_read_data = file.read()
    except Exception as open_exception:
        raise ValueError(f"Unable to read {path_to_python}") from open_exception

    try:
        with open(path_to_output, "w") as target:
            target.write(
                python_minifier.minify(
                    replace_includes(main_file_read_data, path_to_python),
                    remove_literal_statements=True

                )
            )
    except Exception as write_exception:
        raise ValueError(f"Unable to write output file {path_to_output}") from write_exception

    if flash:
        uflash.flash(path_to_output)


def watch_file(path, func, *args, **kwargs):
    """
    Watch a file for changes by polling its last modification time. Call the
    provided function with *args and **kwargs upon modification.
    """
    if not path:
        raise ValueError('Please specify a file to watch')
    print('Watching "{}" for changes'.format(path))
    last_modification_time = os.path.getmtime(path)
    try:
        while True:
            time.sleep(1)
            new_modification_time = os.path.getmtime(path)
            if new_modification_time == last_modification_time:
                continue
            func(*args, **kwargs)
            last_modification_time = new_modification_time
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Build a microbit program")

    parser.add_argument('input',
                        help='Main file',
                        action='store')

    parser.add_argument('--output', '-o',
                        help='Output path',
                        default=path.join(gettempdir(), f"main.py"),
                        action='store')

    parser.add_argument('--no-flash',
                        help='Do not flash microbit',
                        default=False,
                        action='store_true')

    parser.add_argument('-w', '--watch',
                        action='store_true',
                        help='Watch the source file for changes.')

    args = parser.parse_args()
    
    main_file_path = args.input
    output_file_path = args.output
    flash_microbit = not args.no_flash

    if args.watch:
        try:
            watch_file(main_file_path, flash, path_to_python=main_file_path, path_to_output=output_file_path, flash=flash_microbit)
        except Exception as ex:
            error_message = "Error watching {source}: {error!s}"
            print(error_message.format(source=main_file_path, error=ex),
                  file=sys.stderr)
            sys.exit(1)

    else:
        try:
            flash(path_to_python=main_file_path, path_to_output=output_file_path, flash=flash_microbit)
        except Exception as ex:
            error_message = "Error building {source}: {error!s}"
            print(error_message.format(source=main_file_path, error=ex),
                  file=sys.stderr)
            sys.exit(1)