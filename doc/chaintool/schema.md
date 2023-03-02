# Schema of Chaintool's Meta Data
| **column_name** | **data_type** | **description** | **example** |
| --- | --- | --- | --- |
| SUBMITTED_BY | String | Provider's name | Chaintool |
| ADDRESS | String | Cryptocurrency address | 0x4d77a1144dc74f26838b69391a6d3b1e403d0990 |
| CHAIN | String | Cryptocurrency chain type | ETH |
| ENTITY_NAME | String | The real identity of the owner of the address | huobi |
| NAME | String | Further description of ENTITY_NAME | Huobi 26 |
| CATEGORIES | Array | The identity categories of the owner of the address, maybe have multiple values | ["Exchange"] |
| ATTRIBUTES | Array | Describe some dynamic infomation, maybe have multiple values | ["Sanctions", "Stolen Funds"] |
| TAGGED_ON | Datetime | Tag marking time | 2022-12-01 |
