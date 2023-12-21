parse_top = {
    "type": "function",
    "function": {
        "name": "extract_tops_details",
        "description": "Isolate and categorize details about tops from the overall fashion suggestion for subsequent product matching.",
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
        "description": "Focus on extracting specifics about bottoms like trousers or skirts from the fashion suggestion for product matching.",
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
        "description": "Separate and detail jacket-related aspects from the fashion suggestion to aid in finding matching products.",
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
        "description": "Identify and categorize details about shoes from the fashion suggestion for accurate product retrieval.",
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
        "description": "Distinguish and categorize accessory details from the fashion suggestion for relevant product searches.",
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
