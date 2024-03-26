#!/usr/bin/env python3

# Copyright 2023 The chainmetareader Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import click
import jinja2


@click.command()
def taxonomy():
    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="templates"),
        keep_trailing_newline=True,
    )
    taxonomy_template = environment.get_template("taxonomy.md.jinja")

    with open("chainmeta/config/categories.json", "r") as categories_file, open(
        "doc/taxonomy.md", "w+"
    ) as taxonomy_file:
        categories = json.load(categories_file)
        taxonomy_file.write(taxonomy_template.render(categories=categories))

    click.echo(click.style("doc/taxonomy.md updated", fg="green"))


if __name__ == "__main__":
    taxonomy()
