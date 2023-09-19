# Microscope ChainMeta Reader
`chainmeta_reader` is a Python module that loads, validates, and parses chainmeta from Open Chainmeta participants.

## What is Microsocope?
* [Microscope Whitepaper](https://github.com/openchainmeta/chainmetareader/blob/main/Microscope_Whitepaper_V1.pdf)
* [Microscope Taxonomy](https://docs.google.com/document/d/1Y0KminLU9xVGocVoIFHIVfyRS1Nz4tWDjq4RJhVXMW0/edit)
* [Protocol Notion drafts](https://leozc.notion.site/leozc/438374dfd880436eaf996e5897e5ff93)

## Read Chainmeta from Database
Before accessing the Open Chainmeta database, you need to obtain database credentials. Once you have the connection string, you can export it as an environment variable as follows:

```bash
export CHAINMETA_DB_CONN=mysql+pymysql://user:pwd@dbhost/chainmeta
```

Alternatively, you can set the connection string explicitly in your code using `set_connection_string()`:

```
>>> import chainmeta_reader as cm
>>> cm.set_connection_string("mysql+pymysql://user:pwd@dbhost/chainmeta")
```

To read all chainmeta from the database, use `search_chainmeta()`:

```
>>> result_generator = cm.search_chainmeta()
>>> list(result_generator)
```

To filter the chainmeta based on specific attributes, you can pass a filter dictionary to `search_chainmeta()`:

```
>>> filter = {"address": "0xf177aa7b0602f787f6f01c65f4b2e267336fd349", "chain": "ethereum-mainnet"}
>>> result_generator = cm.search_chainmeta(filter=filter)
>>> list(result_generator)
```

This will return a list of chainmeta that match the specified filter.

***Note:*** The `search_chainmeta()` function only returns a generator that lazily loads the chainmeta from the database. Therefore, you need to convert it to a list or iterate over it to access the actual data.

### Read from Local File

You can read chainmeta from a local file using the `load()` function provided by chainmeta_reader. It will load all included artifacts, validate the artifacts, and translate them to common schema. Here's an example:

```
>>> with open("./examples/coinbase_sample.json") as f:
...     metadata = cm.load(f, artifact_base_path="./examples")
...
```

You can access the metadata in common schema via `metadata["chainmetadata"]["artifact"]` and the raw metadata via `metadata["chainmetadata"]["raw_artifact"]`.


## Contribute to Open Chainmeta
If you want to contribute your metadata to the Open Chainmeta database, you can use the `upload_chainmeta()` function provided by chainmeta_reader. Here's an example:

```
>>> common_metadata = metadata["chainmetadata"]["artifact"]
>>> cm.upload_chainmeta(common_metadata)
```

Alternatively, you can use the upload.py script provided by chainmeta_reader to upload chainmeta from a file. Here's an example:
```bash
./upload.py ./examples/coinbase_sample.json
```

This will upload the chainmeta in the ./examples/coinbase_sample.json file to the Open Chainmeta database.

See the [usage.py](https://github.com/openchainmeta/chainmetareader/blob/main/usage.py) file for more details.
