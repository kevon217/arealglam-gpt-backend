import asyncio
import unittest

from app.services.assistant_processing import extract_wardrobe_items


class TestAssistantProcessingIntegration(unittest.TestCase):
    def test_extract_wardrobe_items(self):
        # Sample fashion suggestion
        fashion_suggestion = "A summer beach party outfit could include a floaty kaftan or a breezy linen shirt paired with comfortable shorts, strappy sandals, a wide-brimmed hat, and stylish sunglasses."

        # Call the function under test
        result = asyncio.run(extract_wardrobe_items(fashion_suggestion))
        print(result)
        # Check if the result contains expected keywords
        # Note: The exact content of the result might vary depending on the AI's response
        self.assertTrue(any("kaftan" in item for item in result))
        self.assertTrue(any("linen shirt" in item for item in result))
        self.assertTrue(any("shorts" in item for item in result))
        self.assertTrue(any("sandals" in item for item in result))
        self.assertTrue(any("hat" in item for item in result))
        self.assertTrue(any("sunglasses" in item for item in result))


if __name__ == "__main__":
    unittest.main()
