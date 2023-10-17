# Microscope ChainMeta Reader
`chainmeta_reader` is a Python module that loads, validates, and parses chainmeta from Microscope protocol participants.

## What is Microsocope?
* [Microscope Whitepaper](https://github.com/openchainmeta/chainmetareader/blob/main/Microscope_Whitepaper_V1.pdf)
* [Microscope Taxonomy](https://github.com/openchainmeta/chainmetareader/blob/main/Microsope%20Taxonomy.pdf)
* [Protocol Website](http://microscopeprotocol.xyz/)

## Read Chainmeta from Database
Before accessing Microscope's Open Chainmeta database, you need to obtain database credentials. Once you have the connection string, you can export it as an environment variable as follows:

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


## Contribute Chainmeta to Database
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

## Adding New Categories to Taxonomy
Only categories defined in the [taxonomy](https://github.com/openchainmeta/chainmetareader/blob/main/Microsope%20Taxonomy.pdf) can be used, and this enforcement is maintained through [chainmeta_reader/config/categories.json](https://github.com/microscopexyz/chainmetareader/blob/main/chainmeta_reader/config/categories.json).

Follow these steps, if you need to add new categories to taxonomy:

1. <b>Make a Pull Request (PR)</b>: Create a Pull Request to add the new categories to the categories.json file.

2. <b>Description and Discussion</b>: In your Pull Request, be sure to provide a clear description of why you believe these new categories are needed and how they will be used. This information will help the project maintainers understand the rationale behind your request.

3. <b>Weekly Meeting</b>: All PRs will be discussed in weekly meetings. This means that the project maintainers will review your proposed changes and decide whether to accept or reject them based on the discussion during the meeting.

Remember to follow the contribution guidelines and any specific instructions provided by the maintainers of the project. Additionally, ensure that your proposed categories align with the project's goals and objectives.
