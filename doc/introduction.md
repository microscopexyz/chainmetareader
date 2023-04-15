# Introduction
Chainmeta (blockchain metadata) refers to the labels assigned to blockchain addresses that help identify the entity that the address belongs to, the descriptive name of the address, and the categories that the address belongs to. Open Chainmeta is an open system that allows different users and organizations to contribute and share chainmeta with each other.

## Representation
Chainmeta can be represented in three different flavors, namely metadata in common schema, metadata in custom schema, and metadata in database schema.

Metadata in common schema, also known as the **common schema**, is a standardized format that has been codified in a repository. It consists of the following fields:

```py
class ChainmetaItem:
    # Chain identification
    chain: str

    # Wallet or contract address
    address: str

    # Entity ID of the address
    entity: str

    # Name of the address
    name: Optional[str]

    # Category IDs of the address
    categories: List[str]

    # Source of the metadata
    source: str

    # Submitter of the metadata
    submitted_by: str

    # Last updated time
    submitted_on: str
```

Metadata in custom schema, also known as the **raw metadata**, refers to the arbitrary format in which a participant stores the metadata initially in their own system. Anyone who wants to participate in the Open Chainmeta project must adopt the common schema or provide their custom schema definition and demonstrate how their schema can be translated into the common schema and vice versa.

Metadata in the **database schema** refers to how the metadata is stored in the central database. All metadata contributed by different participants are translated into the common schema. From the common schema, it is flattened into a database record. Participants only need to provide a translation between their custom schema and the common schema, but not between their custom schema and the database schema.
