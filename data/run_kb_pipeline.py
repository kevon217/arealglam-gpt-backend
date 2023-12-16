import os
import sys
import time

# Assuming both scripts are in the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from get_product_data import get_product_data
from create_product_kb import main as create_kb


def run_pipeline():
    print("Starting the data retrieval and knowledge base creation pipeline...")

    # Run the product data retrieval script
    print("Retrieving product data...")
    get_product_data()
    print("Product data retrieval completed.")

    # Adding a short delay to ensure file system sync
    time.sleep(2)

    # Run the knowledge base creation script
    print("Creating product knowledge base...")
    create_kb()
    print("Knowledge base creation completed.")

    print("Pipeline execution finished.")


if __name__ == "__main__":
    run_pipeline()
