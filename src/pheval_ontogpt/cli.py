import click

from pheval_ontogpt.post_process.post_process_results_format import create_standardised_results_command


@click.group()
def main():
    pass


main.add_command(create_standardised_results_command)

if __name__ == "__main__":
    main()
