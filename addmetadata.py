from kiara import Metadata, Version
from DownloadJournals import download_journals
class DownloadJournalsMetadata(Metadata):
    _description: str = "A module to download journals from Europeana using pyeuropeana."
    _version: Version = Version("1.0.0")

download_journals.__kiara_metadata__ = DownloadJournalsMetadata
