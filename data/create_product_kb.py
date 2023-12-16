import json
import os
import glob
import logging


def setup_logging(knowledge_base_dir):
    """Set up logging to file with basic formatting."""
    log_file = os.path.join(knowledge_base_dir, "kb_creation_log.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def format_product(product):
    """Format a single product for GPT retrieval."""
    formatted_text = (
        f"Product ID: {product['id']}\n"
        f"Name: {product['name']}\n"
        f"Description: '{product['pdesc']}'\n"
        f"Price: {product['price']}\n"
        f"Category ID: {product['product_category']['id']}\n"
        f"Category Name: {product['product_category']['name']}\n"
    )
    return formatted_text


def get_latest_output_folder(base_path):
    """Get the latest folder in the output directory."""
    output_dir = os.path.join(base_path, "output")
    all_subdirs = [
        os.path.join(output_dir, d)
        for d in os.listdir(output_dir)
        if os.path.isdir(os.path.join(output_dir, d))
    ]
    return max(all_subdirs, key=os.path.getmtime)


def process_json_files(json_files, knowledge_base_dir):
    for json_file in json_files:
        try:
            with open(json_file, "r") as file:
                products_data = json.load(file)["data"]

            category_id = (
                os.path.basename(json_file).split("_")[-1].replace(".json", "")
            )
            kb_file = os.path.join(
                knowledge_base_dir, f"products_kb_category_{category_id}.txt"
            )
            with open(kb_file, "w", encoding="utf-8") as file:
                for product in products_data:
                    file.write(format_product(product) + "\n\n")

            logging.info(
                f"Knowledge base for Category ID {category_id} created with {len(products_data)} products."
            )

        except Exception as e:
            logging.error(f"Error processing {json_file}: {e}")


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    latest_output_dir = get_latest_output_folder(base_path)

    knowledge_base_dir = os.path.join(latest_output_dir, "knowledge_base_files")
    os.makedirs(knowledge_base_dir, exist_ok=True)

    setup_logging(knowledge_base_dir)

    json_files = glob.glob(
        os.path.join(latest_output_dir, "product_category_id_*.json")
    )
    process_json_files(json_files, knowledge_base_dir)


if __name__ == "__main__":
    main()
