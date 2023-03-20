import pathlib

from chainmeta_reader import (
    ChaintoolTranslator,
    CoinbaseTranslator,
    denormalize,
    load,
    normalize,
)

artifact_base_path = pathlib.Path("./examples")
with open(artifact_base_path.joinpath("coinbase_sample.json")) as f:
    # Load Coinbase artifact
    metadata = load(f, artifact_base_path=artifact_base_path)
    raw_metadata = metadata["chainmetadata"]["loaded_artifact"]

    # Translate to intermediate metadata schema
    intermediate_metadata = normalize(
        metadata["chainmetadata"]["loaded_artifact"], CoinbaseTranslator
    )

    # Translate back to Coinbase metadata schema
    raw_metadata2 = denormalize(intermediate_metadata, CoinbaseTranslator)

with open(artifact_base_path.joinpath("chaintool_sample.json")) as f:
    # Load Chaintool artifact
    metadata = load(f, artifact_base_path=artifact_base_path)
    raw_metadata = metadata["chainmetadata"]["loaded_artifact"]

    # Translate to intermediate metadata schema
    intermediate_metadata = normalize(
        metadata["chainmetadata"]["loaded_artifact"], ChaintoolTranslator
    )

    # Translate back to Chaintool metadata schema
    raw_metadata2 = denormalize(intermediate_metadata, ChaintoolTranslator)
