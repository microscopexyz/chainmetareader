from typing import List
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

class Namespace(Enum):
    ChainTool = 1
    Coinbase = 2
    GoPlus = 3
    
@dataclass
class Network:
    """Network represents a uniquely identified blockchain network, 
    e.g. ethereum mainnet, or ethereum goerli
    """

    # The string representation of the network
    name: str

@dataclass
class Tag:
    """Tag is a generic container for any information like name, 
    entity or category etc.
    """
    
    # Namespace this tag belongs to
    namespace: Namespace

    # Type of the tag, e.g. entity, category or attribute
    type: str               
    
    # The string representation of the tag
    name: str

@dataclass
class MetadataItem:
    """Intermediate representation of the metadata.
    """

    # Wallet or contract address 
    address: str

    # Network identification
    network: Network

    # Single piece of metadata
    tag: Tag

    # Submitter of the metadata
    submitted_by: str

    # Last updated time
    last_updated: datetime


class ITranslator(ABC):
    @abstractmethod
    def to_intermediate(self, raw_metadata) -> List[MetadataItem]:
        """Translate to intermediate representation
        """
        pass

    @abstractmethod
    def from_intermediate(self, intermediate_metadata: List[MetadataItem]) -> object:
        """Translate from intermediate representation
        """
        pass


class CoinbaseTranslator(ITranslator):
    def to_intermediate(self, raw_metadata) -> List[MetadataItem]:
        pass

    def from_intermediate(self, intermediate_metadata: List[MetadataItem]) -> object:
        pass
