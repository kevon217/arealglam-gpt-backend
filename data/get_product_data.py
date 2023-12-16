# get_product_data.py
import requests
import json
import os
from datetime import datetime
from collections import defaultdict
import logging
from termcolor import colored


def setup_logging(output_dir):
    """Set up logging to file with basic formatting for totals."""
    log_file = os.path.join(output_dir, "run_log.log")

    file_logger = logging.getLogger("fileLogger")
    file_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    file_format = logging.Formatter("%(message)s")
    file_handler.setFormatter(file_format)

    file_logger.addHandler(file_handler)
    return file_logger


def create_output_directory():
    """Creates an output directory based on the current datetime in the script's directory."""
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create a directory path for 'output'
    output_base_dir = os.path.join(script_dir, "output")

    # Create a subdirectory with the current datetime
    datetime_dir = datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = os.path.join(output_base_dir, datetime_dir)
    os.makedirs(output_dir, exist_ok=True)

    return output_dir


def categorize_products_by_category_id(products):
    categorized_products = defaultdict(list)
    for product in products:
        category_id = product.get("product_category_id")
        categorized_products[category_id].append(product)
    return categorized_products


def save_categorized_products(categorized_products, output_dir):
    for category_id, products in categorized_products.items():
        file_name = f"product_category_id_{category_id}.json"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            # Wrap the products in a dictionary with the 'data' key
            data_to_save = {"data": products}
            json.dump(data_to_save, file, indent=4)
        print(
            colored(
                f"Saved {len(products)} products in category {category_id} to {file_name}",
                "green",
            )
        )


def get_product_data():
    # API endpoint URL
    url = "https://admin.arealglam.com/api/allproduct"

    # Headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.arealglam.com",
        "Referer": "https://www.arealglam.com/",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()

            output_dir = create_output_directory()
            file_logger = setup_logging(output_dir)

            categorized_products = categorize_products_by_category_id(
                data.get("data", [])
            )
            total_products = sum(
                len(products) for products in categorized_products.values()
            )

            file_logger.info(f"Total products retrieved: {total_products}")

            save_categorized_products(categorized_products, output_dir)

            for category_id, products in categorized_products.items():
                file_logger.info(
                    f"Category ID {category_id} has {len(products)} products."
                )
                print(
                    colored(
                        f"Category ID {category_id} has {len(products)} products.",
                        "yellow",
                    )
                )

        else:
            print(
                colored(
                    f"Failed to fetch data: Status code {response.status_code}", "red"
                )
            )
    except Exception as e:
        print(colored(f"An error occurred: {e}", "red"))


get_product_data()
