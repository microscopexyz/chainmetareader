import csv
import logging

from chainmeta_reader import load, db

# Set logging level
logging.basicConfig(level=logging.INFO)


# 创建一个函数来写入 CSV 文件
def write_csv_file(file_name, data, idx):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # 写入 CSV 表头（如果需要）
        header = ["id", "chain", "address", "namespace", "scope", "tag", "submitted_by", "submitted_on", "source"]
        writer.writerow(header)
        # 写入数据
        for line in data:
            idx = idx + 1
            row_data = []
            row_data.append(idx)
            for ee in line.split(','):
                row_data.append(ee)
            writer.writerow(row_data)
    return idx


# Load metadata from file with Chaintool schema and translate between schemas
def update_json_file(new_file_name):
    # 读取template.json文件
    with open('./examples/chaintool_sample_temp.json', 'r') as file:
        template_data = file.read()

    # 替换占位符
    replaced_data = template_data.replace('btc_data', new_file_name)

    # 写入chainmeta_sample.json文件
    with open('./examples/chaintool_sample.json', 'w') as file:
        file.write(replaced_data)

idx = 0

for idd in range(1, 6):
    logging.info(f"----- {idd} begin.")
    update_json_file(f"btc_{idd}_data")

    with open("./examples/chaintool_sample.json") as f:
        # Load Chaintool artifact
        logging.info("1. Chaintool: Load raw metadata")
        metadata = load(f, artifact_base_path="./examples")

        raw_metadata = metadata["chainmetadata"]["raw_artifact"]

        common_metadata = metadata["chainmetadata"]["artifact"]
        logging.info("2. Translate is ready")

        records = db.flatten(common_metadata)
        content1 = list()
        for record in records:
            line = f"{record.chain},{record.address},{record.namespace},{record.scope},{record.tag},{record.submitted_by},{record.submitted_on},{record.source}"
            content1.append(line)

        logging.info("3. content is ready")

        idx = write_csv_file(f"/Users/sky/chaintool/microscope/chainmeta.chaintool_btc_1.00000{idd}.csv", content1, idx)

        print(f'Total rows of data have been written to CSV files.')
