# OntoGPT Runner for PhEval
This is the OntoGPT plugin for PhEval.

## Developers

An example skeleton `config.yaml` has been provided (`pheval.ontogpt/config.yaml`) which should be correctly filled and moved to the input-dir location.

To install the OntoGPT plugin:

``` 
git clone https://github.com/yaseminbridges/pheval.ontogpt.git
cd pheval.ontogpt/

poetry install
poetry shell
```

## Configuring the prompt

If you wish to alter the prompt given to the API, you can alter the template located in 
`pheval.ontogpt/src/pheval_ontogpt/prompt_templates/template.jinja2`. However, you **must** retain the output format outlined.

## Input directory structure

Where . is the root of the input directory

```tree
.
└── config.yaml
```

## Test data directory structure

Where . is the root of the test data directory

```tree
.
└── phenopackets
   ├── Abdul_Wahab-2016-GCDH-Patient_5.json
   └── Ajmal-2013-BBS1-IV-5_family_A.json

```
