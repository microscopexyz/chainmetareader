import logging

from chainmeta_reader import load, search_chainmeta, upload_chainmeta

# Set logging level
logging.basicConfig(level=logging.INFO)

# Load metadata from file with Coinbase schema
with open("./examples/coinbase_sample.json") as f:
    # Load artifact
    logging.info("1. Load Metadata")
    metadata = load(f, artifact_base_path="./examples")

    # Raw metadata
    raw_metadata = metadata["chainmetadata"]["raw_artifact"]
    for item in raw_metadata:
        logging.info(item)

    # Common schema metadata
    common_metadata = metadata["chainmetadata"]["artifact"]
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
with open("./examples/chaintool_sample.json") as f:
    # Load Chaintool artifact
    logging.info("1. Chaintool: Load raw metadata")
    metadata = load(f, artifact_base_path="./examples")

    # Raw metadata
    raw_metadata = metadata["chainmetadata"]["raw_artifact"]
    for item in raw_metadata:
        logging.info(item)

    # Common schema metadata
    logging.info("2. Chaintool: Translate to common metadata")
    common_metadata = metadata["chainmetadata"]["artifact"]
    for item in common_metadata:
        logging.info(item)

    # Translate back to Chaintool schema
    from chainmeta_reader.contrib.chaintool import ChaintoolTranslator
    logging.info("3. Chaintool: Translate back to Chaintool schema")
    raw_metadata = [
        ChaintoolTranslator().from_common_schema(i) for i in common_metadata
    ]
    for item in raw_metadata:
        logging.info(item)

    # # Persist metadata to database
    logging.info("4. Chaintool: Upload to database")
    n = upload_chainmeta(common_metadata)
    logging.info(f"Added {n} items to database")

    # Retrieve metadata from database
    logging.info("5. Chaintool: Search without filter")
    result = search_chainmeta()
    for i, item in enumerate(result):
        if i >= 10:
            break
        logging.info(item)

    # Retrieve metadata from database with filter
    logging.info("6. Search with filter")
    result = search_chainmeta(
        filter={
            "address": "0xd73330336d084FaDF67cF8DE0EF4fB138cD642C9",
            "chain": "ethereum_mainnet",
        }
    )
    for item in result:
        logging.info(item)
