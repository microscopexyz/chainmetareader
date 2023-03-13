# ChainMeta Reader
`chainmeta_reader` loads, validates and parses block chain metadata from supported metadata files.

```
>>> import chainmeta_reader
>>> import pathlib
>>> artifact_base_path = pathlib.Path("./examples")
>>> with open(artifact_base_path.joinpath("coinbase_sample.json")) as f:
...     metadata = chainmeta_reader.load(f, artifact_base_path=artifact_base_path)
...
>>> metadata["provider"]
{'provider_name': 'coinbase', 'provider_id': 'ocm000002', 'provider_signature': ''}
>>>
>>> metadata["chainmetadata"]["loaded_artifact"][0]
{'address': '0xf177aa7b0602f787f6f01c65f4b2e267336fd349', 'network_name': 'ethereum-mainnet', 'entity': 'Uniswap', 'name': 'Uniswap V2: Hmf', 'categories': ['defi', 'dex'], 'submitted_by': 'coinbase', 'last_updated': '2022-09-21 00:00:00'}
>>> metadata["chainmetadata"]["loaded_artifact"][1]
{'address': '0xd62f1beba129440c5c07e4fb597ec1f61260d26b', 'network_name': 'ethereum-mainnet', 'entity': 'Uniswap', 'name': 'Uniswap V2: $Ashiba', 'categories': ['defi', 'dex', 'erc20 token'], 'submitted_by': 'coinbase', 'last_updated': '2022-09-21 00:00:00'}
>>>
>>> intermediate_metadata = chainmeta_reader.normalize(metadata["chainmetadata"]["loaded_artifact"], chainmeta_reader.CoinbaseTranslator)
>>> intermediate_metadata
<generator object normalize at 0x105386eb0>
>>> list(intermediate_metadata)
[MetadataItem(address='0xf177aa7b0602f787f6f01c65f4b2e267336fd349', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='entity', name='Uniswap'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00'), MetadataItem(address='0xf177aa7b0602f787f6f01c65f4b2e267336fd349', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='name', name='Uniswap V2: Hmf'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00'), MetadataItem(address='0xf177aa7b0602f787f6f01c65f4b2e267336fd349', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='category', name='defi'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00'), MetadataItem(address='0xf177aa7b0602f787f6f01c65f4b2e267336fd349', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='category', name='dex'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00'), MetadataItem(address='0xd62f1beba129440c5c07e4fb597ec1f61260d26b', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='entity', name='Uniswap'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00'), MetadataItem(address='0xd62f1beba129440c5c07e4fb597ec1f61260d26b', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='name', name='Uniswap V2: $Ashiba'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00'), MetadataItem(address='0xd62f1beba129440c5c07e4fb597ec1f61260d26b', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='category', name='defi'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00'), MetadataItem(address='0xd62f1beba129440c5c07e4fb597ec1f61260d26b', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='category', name='dex'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00'), MetadataItem(address='0xd62f1beba129440c5c07e4fb597ec1f61260d26b', network=Network(name='ethereum-mainnet'), tag=Tag(namespace='cb', type='category', name='erc20 token'), submitted_by='coinbase', last_updated='2022-09-21 00:00:00')]
>>>
>>> raw_metadata = chainmeta_reader.denormalize(intermediate_metadata, chainmeta_reader.CoinbaseTranslator)
>>> raw_metadata
<generator object denormalize at 0x1012aa120>
>>> list(raw_metadata)
[{'categories': ['defi', 'dex'], 'address': '0xf177aa7b0602f787f6f01c65f4b2e267336fd349', 'network_name': Network(name='ethereum-mainnet'), 'submitted_by': 'coinbase', 'last_updated': '2022-09-21 00:00:00', 'entity': 'Uniswap', 'name': 'Uniswap V2: Hmf'}, {'categories': ['defi', 'dex', 'erc20 token'], 'address': '0xd62f1beba129440c5c07e4fb597ec1f61260d26b', 'network_name': Network(name='ethereum-mainnet'), 'submitted_by': 'coinbase', 'last_updated': '2022-09-21 00:00:00', 'entity': 'Uniswap', 'name': 'Uniswap V2: $Ashiba'}]
```
