import unittest

from pheval.post_processing.post_processing import PhEvalDiseaseResult

from pheval_ontogpt.post_process.post_process_results_format import PhEvalDiseaseResultFromOntoGPT

ontogpt_result = {
    "disease": "Glutaric Aciduria Type I",
    "omim_disease_id": "231670",
    "score": 0.8,
    "rank": 1,
    "phenotypes": [
        "Macrocephaly",
        "Cerebral atrophy",
        "Subdural hemorrhage",
        "Glutaric aciduria",
        "Dystonia",
    ],
    "disease_ids": ["MONDO:0009281"],
}
ontogpt_results = [
    {
        "disease": "Glutaric Aciduria Type I",
        "omim_disease_id": "231670",
        "score": 0.8,
        "rank": 1,
        "phenotypes": [
            "Macrocephaly",
            "Cerebral atrophy",
            "Subdural hemorrhage",
            "Glutaric aciduria",
            "Dystonia",
        ],
        "disease_ids": ["MONDO:0009281"],
    },
    {
        "disease": "Glutaryl-CoA dehydrogenase deficiency",
        "omim_disease_id": "231680",
        "score": 0.6,
        "rank": 2,
        "phenotypes": ["Cerebral atrophy", "Glutaric aciduria", "Dystonia"],
        "disease_ids": ["MONDO:0009281", "MONDO:0009281"],
    },
]


class TestPhEvalDiseaseResultFromOntoGPT(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.disease_result = PhEvalDiseaseResultFromOntoGPT(ontogpt_results)

    def test_obtain_score(self):
        self.assertEqual(self.disease_result.obtain_score(ontogpt_result), 0.8)

    def test_obtain_disease_name(self):
        self.assertEqual(
            self.disease_result.obtain_disease_name(ontogpt_result), "Glutaric Aciduria Type I"
        )

    def test_obtain_omim_disease_id(self):
        self.assertEqual(self.disease_result.obtain_omim_disease_id(ontogpt_result), "231670")

    def test_extract_pheval_requirements(self):
        self.assertEqual(
            self.disease_result.extract_pheval_requirements(),
            [
                PhEvalDiseaseResult(
                    disease_name="Glutaric Aciduria Type I", disease_identifier="231670", score=0.8
                ),
                PhEvalDiseaseResult(
                    disease_name="Glutaryl-CoA dehydrogenase deficiency",
                    disease_identifier="231680",
                    score=0.6,
                ),
            ],
        )
