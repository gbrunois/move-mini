#!/usr/bin/env python3

import argparse
import re
from os.path import join
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Build a microbit program")

    parser.add_argument('input',
                        help='Main file',
                        action='store')

    parser.add_argument('--output', '-o',
                        help='Output path',
                        default=join(gettempdir(), f"main.py"),
                        action='store')

    parser.add_argument('--no-flash',
                        help='Do not flash microbit',
                        default=False,
                        action='store_true')

    args = parser.parse_args()
    
    main_file_path = args.input
    output_file_path = args.output
    flash_microbit = not args.no_flash

    try:
        with open(main_file_path, 'r') as file:
            main_file_read_data = file.read()
    except Exception as open_exception:
        raise ValueError(f"Unable to read {main_file_path}") from open_exception

    try:
        with open(output_file_path, "w") as target:
            target.write(
                python_minifier.minify(
                    replace_includes(main_file_read_data, main_file_path),
                    remove_literal_statements=True

                )
            )
    except Exception as write_exception:
        raise ValueError(f"Unable to write output file {output_file_path}") from write_exception

    if flash_microbit:
        uflash.flash(output_file_path)
