"""OntoGPT Runner"""

from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner

from pheval_ontogpt.construct_run_metadata.construct_metadata import construct_run_metadata
from pheval_ontogpt.post_process.post_process import post_process_results_format
from pheval_ontogpt.run.run import run_basic
from pheval_ontogpt.tool_specific_configuration_parser import OntoGPTToolSpecificConfigurations


@dataclass
class OntoGPTPhEvalRunner(PhEvalRunner):
    """_summary_"""

    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path
    version: str

    def prepare(self):
        """prepare"""
        print("preparing")

    def run(self):
        """run"""
        print("running with OntoGPT")
        tool_specific_configurations = OntoGPTToolSpecificConfigurations.parse_obj(
            self.input_dir_config.tool_specific_configuration_options
        )
        run_basic(
            self.testdata_dir,
            self.raw_results_dir,
            tool_specific_configurations.model,
            self.input_dir.joinpath(tool_specific_configurations.template),
            (
                self.input_dir.joinpath(tool_specific_configurations.constrained_list_path)
                if tool_specific_configurations.constrained_list_path is not None
                else None
            ),
        )

    def post_process(self):
        """post_process"""
        print("post processing")
        post_process_results_format(
            self.raw_results_dir,
            self.output_dir,
            self.input_dir_config.gene_analysis,
            self.input_dir_config.disease_analysis,
        )

    def construct_meta_data(self):
        tool_specific_configurations = OntoGPTToolSpecificConfigurations.parse_obj(
            self.input_dir_config.tool_specific_configuration_options
        )
        return construct_run_metadata(self.meta_data, tool_specific_configurations.model)
