from phenopackets import Phenopacket
from pheval.utils.phenopacket_utils import PhenopacketUtil


class PhenopacketCleaner:
    """
    Class for 'cleaning' a phenopacket from any disease-identifying elements including:
    disease and interpretation objects,
    """
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
        """Remove the evidence for an assertion of the observed phenotype."""
        for phenotypic_feature in PhenopacketUtil(self.phenopacket).phenotypic_features():
            del phenotypic_feature.evidence[:]

    def clear_meta_data(self):
        """Clear the meta_data element from phenopacket."""
        self.phenopacket.meta_data.Clear()

    def clear_taxonomy(self):
        """Clear the taxonomy element from phenopacket."""
        self.phenopacket.subject.taxonomy.Clear()

    def remove_files(self):
        """Remove files object from phenopacket."""
        del self.phenopacket.files[:]

    def clean_phenopacket(self) -> Phenopacket:
        """Clean a phenopacket from extra elements not required for disease prediction."""
        self.remove_evidence_from_phenotypic_features()
        self.remove_interpretations()
        self.remove_diseases()
        self.rename_id()
        self.clear_taxonomy()
        self.clear_meta_data()
        self.remove_files()
        return self.phenopacket
