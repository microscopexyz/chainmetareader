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
from pathlib import Path
import logging

from chainmeta_reader import load, upload_chainmeta

# Set logging level
logging.basicConfig(level=logging.DEBUG)

@click.command()
@click.argument('filename', type=click.Path(exists=True))
def upload(filename: str):

    folder_path = Path(filename).resolve().parent
    with open(filename) as f:
        metadata = load(f, artifact_base_path=folder_path)
        common_metadata = metadata["chainmetadata"]["artifact"]
        n = upload_chainmeta(common_metadata)
        click.echo(click.style(f"Added {n} items to database", fg="green"))

if __name__ == "__main__":
    upload()
