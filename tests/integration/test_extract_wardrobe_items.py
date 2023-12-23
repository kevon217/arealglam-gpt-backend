import asyncio
import unittest
import re
from app.services.assistant_processing import extract_wardrobe_items


def item_exists_in_test(item, items_lols):
    compiled_pattern = re.compile(item, re.IGNORECASE)
    # Flatten the list of lists into a single list
    flattened_items = [element for sublist in items_lols for element in sublist]
    return any(compiled_pattern.search(each_item) for each_item in flattened_items)


class TestAssistantProcessingIntegration(unittest.TestCase):
    def test_extract_wardrobe_items(self):
        fashion_suggestion = "A summer beach party outfit could include a floaty kaftan or a breezy linen shirt paired with comfortable shorts, strappy sandals, a wide-brimmed hat, and stylish sunglasses."
        test_items = [
            "kaftan",
            "linen shirt",
            "shorts",
            "sandals",
            "hat",
            "sunglasses",
            "test_fail",
        ]

        items_lols = asyncio.run(extract_wardrobe_items(fashion_suggestion))
        print(items_lols)

        assertions = {
            item: item_exists_in_test(item, items_lols) for item in test_items
        }
        for item, result in assertions.items():
            print(f"{item}: {'Found' if result else 'Not Found'}")


if __name__ == "__main__":
    unittest.main()
