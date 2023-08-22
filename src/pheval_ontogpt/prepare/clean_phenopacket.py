from phenopackets import Phenopacket
from pheval.utils.phenopacket_utils import PhenopacketUtil
import random


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

    def remove_evidence_from_phenotypic_features(self):
        for phenotypic_feature in PhenopacketUtil(self.phenopacket).phenotypic_features():
            del phenotypic_feature.evidence[:]

    def check_length_phenotypic_features(self):
        if len(PhenopacketUtil(self.phenopacket).phenotypic_features()) > 50:
            selected = random.sample(PhenopacketUtil(self.phenopacket).phenotypic_features(), 50)
            del self.phenopacket.phenotypic_features[:]
            self.phenopacket.phenotypic_features.extend(selected)

    def remove_metadata_resources(self):
        del self.phenopacket.meta_data.resources[:]

    def remove_files(self):
        del self.phenopacket.files[:]

    def clean_phenopacket(self) -> Phenopacket:
        """Clean phenopacket."""
        self.remove_evidence_from_phenotypic_features()
        self.check_length_phenotypic_features()
        self.remove_interpretations()
        self.remove_diseases()
        self.rename_id()
        self.remove_metadata_resources()
        self.remove_files()
        return self.phenopacket
