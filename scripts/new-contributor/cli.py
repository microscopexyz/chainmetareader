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

import click
import jinja2


@click.argument("name", required=True)
@click.command()
def newContributor(name: str):
    name = name.title()
    name_lower = name.lower()

    environment = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="templates"),
        keep_trailing_newline=True,
    )
    schema_template = environment.get_template("example_schema.json.template")
    code_template = environment.get_template("example.py.template")

    with open(f"chainmeta_reader/contrib/{name_lower}_schema.json", "w+") as f:
        f.write(schema_template.render(name=name, name_lower=name_lower))

    with open(f"chainmeta_reader/contrib/{name_lower}.py", "w+") as f:
        f.write(code_template.render(name=name, name_lower=name_lower))

    click.echo(click.style("Created:", fg="green"))
    click.echo(click.style(f"\tcontrib/{name_lower}_schema.json", fg="green"))
    click.echo(click.style(f"\tcontrib/{name_lower}.py", fg="green"))


if __name__ == "__main__":
    newContributor()
