import logging
import pathlib

from chainmeta_reader import (
    ChaintoolTranslator,
    Translator,
    denormalize,
    load,
    normalize,
    search_chainmeta,
    set_artifact_base_path,
    set_connection_string,
    upload_chainmeta,
)

# Set logging level
logging.basicConfig(level=logging.INFO)

# Set database connection string and artifact base path
set_connection_string("mysql+pymysql://root:test@localhost/mysql")
set_artifact_base_path(pathlib.Path("./examples"))

# Load metadata from file with Coinbase schema
with open("./examples/coinbase_sample.json") as f:
    # Load Coinbase artifact
    metadata = load(f)
    raw_metadata = metadata["chainmetadata"]["loaded_artifact"]

    # Translate to common schema
    common_metadata_generator = normalize(
        metadata["chainmetadata"]["loaded_artifact"], Translator()
    )
    common_metadata = [i for i in common_metadata_generator]
    logging.info("1. Metadata in common schema")
    for item in common_metadata:
        logging.info(item)

    # Persist metadata to database
    logging.info("2. Upload to database")
    n = upload_chainmeta(common_metadata)
    logging.info(f"Added {n} items to database")

    # Retrieve metadata from database
    logging.info("3. Search without filter")
    result = search_chainmeta()
    for i, item in enumerate(result):
        if i >= 10:
            break
        logging.info(item)

    # Retrieve metadata from database with filter
    logging.info("4. Search with filter")
    result = search_chainmeta(
        filter={
            "address": "0xf177aa7b0602f787f6f01c65f4b2e267336fd349",
            "chain": "ethereum_mainnet",
        }
    )
    for item in result:
        logging.info(item)

# Load metadata from file with Chaintool schema and translate between schemas
logging.info("5. Translate between schemas")
with open("./examples/chaintool_sample.json") as f:
    # Load Chaintool artifact
    metadata = load(f)
    raw_metadata = metadata["chainmetadata"]["loaded_artifact"]

    # Translate to common schema
    common_metadata_generator = normalize(
        metadata["chainmetadata"]["loaded_artifact"], ChaintoolTranslator()
    )

    # Translate back to Chaintool schema
    common_metadata = [i for i in common_metadata_generator]
    raw_metadata = denormalize(common_metadata, ChaintoolTranslator())
    logging.info([i for i in raw_metadata])
