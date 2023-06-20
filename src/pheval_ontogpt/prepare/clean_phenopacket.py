from phenopackets import Phenopacket


class PhenopacketCleaner:
    def __init__(self, phenopacket: Phenopacket):
        self.phenopacket = phenopacket

    def remove_interpretations(self) -> None:
        """Remove the interpretations object from a phenopacket."""
        del self.phenopacket.interpretations[:]

    def remove_diseases(self) -> None:
        """Remove the diseases object from a phenopacket."""
        del self.phenopacket.diseases[:]

    def rename_id(self) -> None:
        """Rename the ID for the phenopacket."""
        self.phenopacket.id = "patient1"

    def clean_phenopacket(self) -> Phenopacket:
        """Clean phenopacket."""
        self.remove_interpretations()
        self.remove_diseases()
        self.rename_id()
        return self.phenopacket
