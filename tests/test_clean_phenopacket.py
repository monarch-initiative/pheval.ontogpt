import unittest
from copy import copy

from phenopackets import (
    Diagnosis,
    Disease,
    File,
    GeneDescriptor,
    GenomicInterpretation,
    Individual,
    Interpretation,
    MetaData,
    OntologyClass,
    Phenopacket,
    PhenotypicFeature,
    Resource,
    VariantInterpretation,
    VariationDescriptor,
    VcfRecord,
)

from pheval_ontogpt.prepare.clean_phenopacket import PhenopacketCleaner

interpretations = [
    Interpretation(
        id="test-subject-1-int",
        progress_status="SOLVED",
        diagnosis=Diagnosis(
            genomic_interpretations=[
                GenomicInterpretation(
                    subject_or_biosample_id="test-subject-1",
                    interpretation_status=4,
                    variant_interpretation=VariantInterpretation(
                        acmg_pathogenicity_classification="NOT_PROVIDED",
                        therapeutic_actionability="UNKNOWN_ACTIONABILITY",
                        variation_descriptor=VariationDescriptor(
                            gene_context=GeneDescriptor(value_id="NCBIGene:2245", symbol="FGD1"),
                            vcf_record=VcfRecord(
                                genome_assembly="GRCh37",
                                chrom="X",
                                pos=54492285,
                                ref="C",
                                alt="T",
                            ),
                            allelic_state=OntologyClass(
                                id="GENO:0000134",
                                label="hemizygous",
                            ),
                        ),
                    ),
                ),
                GenomicInterpretation(
                    subject_or_biosample_id="test-subject-1",
                    interpretation_status=4,
                    variant_interpretation=VariantInterpretation(
                        acmg_pathogenicity_classification="NOT_PROVIDED",
                        therapeutic_actionability="UNKNOWN_ACTIONABILITY",
                        variation_descriptor=VariationDescriptor(
                            gene_context=GeneDescriptor(value_id="HGNC:18654", symbol="RTTN"),
                            vcf_record=VcfRecord(
                                genome_assembly="GRCh37",
                                chrom="18",
                                pos=67691994,
                                ref="G",
                                alt="A",
                            ),
                            allelic_state=OntologyClass(
                                id="GENO:0000402", label="compound heterozygous"
                            ),
                        ),
                    ),
                ),
            ]
        ),
    )
]

phenotypic_features_with_excluded = [
    PhenotypicFeature(type=OntologyClass(id="HP:0000256", label="Macrocephaly")),
    PhenotypicFeature(type=OntologyClass(id="HP:0002059", label="Cerebral atrophy")),
    PhenotypicFeature(type=OntologyClass(id="HP:0100309", label="Subdural hemorrhage")),
    PhenotypicFeature(type=OntologyClass(id="HP:0003150", label="Glutaric aciduria")),
    PhenotypicFeature(type=OntologyClass(id="HP:0001332", label="Dystonia")),
    PhenotypicFeature(
        type=OntologyClass(id="HP:0008494", label="Inferior lens subluxation"), excluded=True
    ),
]

phenopacket_files = [
    File(
        uri="test/path/to/test_1.vcf",
        file_attributes={"fileFormat": "vcf", "genomeAssembly": "GRCh37"},
    ),
    File(
        uri="test_1.ped",
        file_attributes={"fileFormat": "PED", "genomeAssembly": "GRCh37"},
    ),
]

phenopacket_metadata = MetaData(
    created_by="pheval-converter",
    resources=[
        Resource(
            id="hp",
            name="human phenotype ontology",
            url="http://purl.obolibrary.org/obo/hp.owl",
            version="hp/releases/2019-11-08",
            namespace_prefix="HP",
            iri_prefix="http://purl.obolibrary.org/obo/HP_",
        )
    ],
    phenopacket_schema_version="2.0",
)
phenopacket = Phenopacket(
    id="test-subject",
    subject=Individual(id="test-subject-1", sex=1),
    phenotypic_features=phenotypic_features_with_excluded,
    interpretations=interpretations,
    diseases=[
        Disease(
            term=OntologyClass(
                id="OMIM:612567",
                label="Inflammatory bowel disease 25, early onset, autosomal recessive",
            )
        )
    ],
    files=phenopacket_files,
    meta_data=phenopacket_metadata,
)


class TestPhenopacketCleaner(unittest.TestCase):
    def test_remove_interpretations(self):
        phenopacket_cleaner = PhenopacketCleaner(copy(phenopacket))
        phenopacket_cleaner.remove_interpretations()
        self.assertEqual(
            phenopacket_cleaner.phenopacket,
            Phenopacket(
                id="test-subject",
                subject=Individual(id="test-subject-1", sex=1),
                phenotypic_features=phenotypic_features_with_excluded,
                diseases=[
                    Disease(
                        term=OntologyClass(
                            id="OMIM:612567",
                            label="Inflammatory bowel disease 25, early onset, autosomal recessive",
                        )
                    )
                ],
                files=phenopacket_files,
                meta_data=phenopacket_metadata,
            ),
        )

    def test_remove_diseases(self):
        phenopacket_cleaner = PhenopacketCleaner(copy(phenopacket))
        phenopacket_cleaner.remove_diseases()
        self.assertEqual(
            phenopacket_cleaner.phenopacket,
            Phenopacket(
                id="test-subject",
                subject=Individual(id="test-subject-1", sex=1),
                phenotypic_features=phenotypic_features_with_excluded,
                interpretations=interpretations,
                files=phenopacket_files,
                meta_data=phenopacket_metadata,
            ),
        )

    def test_rename_id(self):
        phenopacket_cleaner = PhenopacketCleaner(copy(phenopacket))
        phenopacket_cleaner.rename_id()
        self.assertEqual(
            phenopacket_cleaner.phenopacket,
            Phenopacket(
                id="patient1",
                subject=Individual(id="test-subject-1", sex=1),
                phenotypic_features=phenotypic_features_with_excluded,
                interpretations=interpretations,
                diseases=[
                    Disease(
                        term=OntologyClass(
                            id="OMIM:612567",
                            label="Inflammatory bowel disease 25, early onset, autosomal recessive",
                        )
                    )
                ],
                files=phenopacket_files,
                meta_data=phenopacket_metadata,
            ),
        )

    def test_clean_phenopacket(self):
        phenopacket_cleaner = PhenopacketCleaner(copy(phenopacket))
        phenopacket_cleaner.clean_phenopacket()
        self.assertEqual(
            phenopacket_cleaner.phenopacket,
            Phenopacket(
                id="patient1",
                subject=Individual(id="test-subject-1", sex=1),
                phenotypic_features=phenotypic_features_with_excluded,
                files=phenopacket_files,
                meta_data=phenopacket_metadata,
            ),
        )
