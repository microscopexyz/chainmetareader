import json
import jsonschema
import os

# Example JSON object to validate
json_obj = {
    "community": "openchainmeta",
    "provider": {
        "provider_name": "xxx",
        "provider_id": "ocm111111",
        "provider_signature": "111111"
    },
    "version": "openchainmeta01",
    "revision": 1,
    "introduction":
    "validating: https://github.com/openchainmeta/chainmetareader/blob/main/chainmeta_reader/meta_schema.json",
    "chainmetadata": {
        "schema": "111",
        "artifact": [{
            "artifact_type": "oss",
            "path": "http://xxxx",
            "fileformat": "csv",
            "signature": "xxxxx"
        },{
            "artifact_type": "remote path",
            "path": "http://xxxx",
            "fileformat": "json",
            "signature": "xxxxx"
        },{
            "artifact_type": "oss",
            "path": "http://xxxx",
            "fileformat": "parquet",
            "signature": "xxxxx"
        }]
    }
}

def main():
    try:
        schema_path = os.path.dirname(os.path.abspath(__file__)) + '/meta_schema.json'
        # Load the JSON schema from an external file
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        jsonschema.validate(json_obj, schema)
        print("Validation successful!")
    except jsonschema.exceptions.ValidationError as e:
        print("Validation error:", e)


if __name__ == '__main__':
    # Validate the JSON object against the schema
    main()