from pathlib import Path

from pheval_ontogpt.post_process.post_process_results_format import create_standardised_results


def post_process_results_format(raw_results_dir: Path, output_dir: Path, gene_analysis: bool, disease_analysis: bool):
    """Create pheval disease result from OntoGPT json output."""
    print("...creating pheval results format...")
    create_standardised_results(
        raw_results_dir=raw_results_dir,
        output_dir=output_dir,
        gene_analysis=gene_analysis,
        disease_analysis=disease_analysis
    )
    print("done")
