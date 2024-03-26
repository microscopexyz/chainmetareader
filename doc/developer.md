# Developer Guide

## Before Commit

Before committing any changes, you should always run the pre-commit and test scripts to ensure that your code is properly formatted and passes all tests.

To run the pre-commit script, use the following command:
```bash
make pre-commit
```

This will check your code against the pre-commit hooks defined in the .pre-commit-config.yaml file. If there are any issues, the script will output an error message and suggest fixes.

To run the tests, use the following command:

```bash
make test
```

This will run all the unit tests defined in the tests/ directory and report any failures or errors.

Both pre-commit and test are part of the CI pipeline, and your pull request will be blocked if they fail. Therefore, it's a good practice to run them locally before creating a pull request to ensure that your changes pass these tests.

## Local Development

To run a database locally
```bash
make db
```

To run the db migration
```bash
make db-migrate
```

To run usage examples interactively
```bash
python -i usage.py
```

## Adding a New Participant

To add a new participant to the Open Chainmeta project, you need to provide the schema definition for your custom schema and the code to translate chainmeta between the common schema and your custom schema. The chainmeta module provides a convenient way to add a new participant using the `make new-contributor` command. Here's an example:

```
make new-contributor name=your_organization
```

This command will generate two files in the chainmeta/contrib/ directory:

- `your_organization_schema.json`: This file contains the schema definition for your custom schema. You need to complete this file by providing the appropriate field names and data types for your schema.

- `your_organization.py`: This file contains the translation code to convert chainmeta between the common schema and your custom schema. You need to complete this file by implementing the from_common_schema() and to_common_schema() functions.

Once you have completed these files, they will be automatically loaded by the chainmeta module.
