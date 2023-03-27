# ChainMeta Reader
`chainmeta_reader` loads, validates and parses block chain metadata from supported metadata sources.

## Consume Block Chain Metadata
Common setup:
```
>>> import chainmeta_reader as cm
>>> cm.set_connection_string("mysql+pymysql://root:test@db/mysql")
>>> cm.set_artifact_base_path(pathlib.Path("./examples"))
```

### Read from Chain Meta Database
Load blockchain metadata from database:
```
>>> result_generator = cm.search_chainmeta()
>>> list(result_generator)
```

Load blockchain metadata from database with filter:
```
>>> result_generator = search_chainmeta(filter={"address": "0xf177aa7b0602f787f6f01c65f4b2e267336fd349", "chain": "ethereum-mainnet"})
>>> list(result_generator)
```

### Read from Local File
Load blockchain metadata from file with opinionated schema:
```
>>> with open("./examples/coinbase_sample.json") as f:
...     metadata = cm.load(f)
...
```

Translate into common metadata:
```
>>> common_metadata_generator = cm.normalize(metadata["chainmetadata"]["loaded_artifact"], cm.CoinbaseTranslator)
```

Translate back into opinionated schema:
```
>>> raw_metadata = cm.denormalize(common_metadata_generator, cm.CoinbaseTranslator)
>>> list(raw_metadata)
```

## Contribute Block Chain Metadata

Translate to common metadata schema:
```
>>> common_metadata_generator = cm.normalize(metadata["chainmetadata"]["loaded_artifact"], cm.CoinbaseTranslator)
```

Upload to database:
```
>>> cm.upload_chainmeta(common_metadata_generator)
```

See Also `usage.py` for details.
