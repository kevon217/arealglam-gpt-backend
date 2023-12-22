parse_top = {
    "type": "function",
    "function": {
        "name": "extract_tops_details",
        "description": "Isolate and categorize details about tops from the overall fashion suggestion for subsequent product matching, while avoiding duplication of items already extracted.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Detailed attributes of tops, such as style, color, and fabric, as extracted from the fashion suggestion.",
                }
            },
            "required": ["description"],
        },
    },
}

parse_bottom = {
    "type": "function",
    "function": {
        "name": "extract_bottoms_details",
        "description": "Focus on extracting specifics about bottoms like trousers or skirts from the fashion suggestion for product matching, while avoiding duplication of items already extracted.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Details about bottoms, including style, fit, and material, as identified in the fashion suggestion.",
                }
            },
            "required": ["description"],
        },
    },
}


parse_jacket = {
    "type": "function",
    "function": {
        "name": "extract_jackets_details",
        "description": "Separate and detail jacket-related aspects from the fashion suggestion to aid in finding matching products, while avoiding duplication of items already extracted.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Characteristics of jackets, such as material, cut, and style, as derived from the fashion suggestion.",
                }
            },
            "required": ["description"],
        },
    },
}


parse_shoes = {
    "type": "function",
    "function": {
        "name": "extract_shoes_details",
        "description": "Identify and categorize details about shoes from the fashion suggestion for accurate product retrieval, while avoiding duplication of items already extracted.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Specifics about shoes, including type, occasion, and style, as mentioned in the fashion suggestion.",
                }
            },
            "required": ["description"],
        },
    },
}


parse_accessories = {
    "type": "function",
    "function": {
        "name": "extract_accessories_details",
        "description": "Distinguish and categorize accessory details from the fashion suggestion for relevant product searches, while avoiding duplication of items already extracted.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Details of accessories, like type and style, as they are described in the fashion suggestion.",
                }
            },
            "required": ["description"],
        },
    },
}


wardrobe_tools = [parse_top, parse_bottom, parse_jacket, parse_shoes, parse_accessories]

format_wardrobe_response = {
    "name": "format_wardrobe_response",
    "description": "Format the found products into a structured JSON response. This function should be used when one or more relevant products are identified in the knowledge base.",
    "parameters": {
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "productID": {
                            "type": "integer",
                            "description": "The unique identifier of the product.",
                        },
                        "description": {
                            "type": "string",
                            "description": "A brief description of the product.",
                        },
                    },
                    "required": ["productID", "description"],
                },
                "description": "A list of product details. This list should contain at least one product when relevant matches are found.",
            }
        },
        "required": ["products"],
    },
}

format_empty_wardrobe_response = {
    "name": "format_empty_wardrobe_response",
    "description": "Generate a structured JSON response with an empty product list. Use this function when no relevant products are found in the knowledge base, indicating a null result.",
    "parameters": {
        "type": "object",
        "properties": {
            "empty_response": {
                "type": "object",
                "properties": {
                    "wardrobe_retrieval": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "description": "An empty array indicating no products were found during the search.",
                        },
                    }
                },
                "description": "An object representing an empty product list, used to indicate that no matching products were identified.",
            }
        },
        "required": ["empty_response"],
    },
}
