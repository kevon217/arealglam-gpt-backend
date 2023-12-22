parse_top = {
    "type": "function",
    "function": {
        "name": "extract_tops_details",
        "description": "Apply this function to each distinct top item or style mentioned in the fashion suggestion. If multiple options are suggested (e.g., 'kaftan or shirt'), treat each as a separate function call.",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Detailed attributes of top, such as style, color, and fabric, as extracted from the fashion suggestion.",
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
        "description": "Use this function for each different bottom item or style specified in the fashion suggestion. Multiple options for bottoms should be processed individually.",
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
        "description": "This function should be applied to each unique jacket item or style present in the fashion suggestion. If various jacket options are given, address each one separately.",
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
        "description": "Engage this function for each specific shoe item or style identified in the fashion suggestion. Separate multiple shoe options and process them individually.",
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
        "description": "Utilize this function for every distinct accessory item or style mentioned. If accessories are grouped (e.g., 'hat, sunglasses'), apply the function to each accessory separately.",
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
    "description": "This function should be used when one or more relevant products are identified in the knowledge base. Format the found products into a structured JSON response.",
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
        "required": [],
    },
}

format_empty_wardrobe_response = {
    "name": "format_empty_wardrobe_response",
    "description": "Use this function when no relevant products are found in the knowledge base, indicating a null result. Generate a structured JSON response with an empty product list.",
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
        "required": [],
    },
}
