# # mapping.py
# import logging

# # Configure Logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger("VTO-Mapping")

# # ==================================================
# # SIZE MAPPING FOR VIRTUAL TRY-ON
# # Categories: tshirts, pants, jackets, shoes
# # Brands: nike, adidas, zara
# # ==================================================

# CATEGORY_SIZE_MAP = {

#     # =======================
#     # T-SHIRTS
#     # =======================
#     "tshirts": {
#         "male": {
#             "nike": {
#                 "S": {"adidas": "44", "zara": "S"},
#                 "M": {"adidas": "46", "zara": "M"},
#                 "L": {"adidas": "48", "zara": "L"},
#             },
#             "adidas": {
#                 "44": {"nike": "S", "zara": "S"},
#                 "46": {"nike": "M", "zara": "M"},
#                 "48": {"nike": "L", "zara": "L"},
#             },
#             "zara": {
#                 "S": {"nike": "S", "adidas": "44"},
#                 "M": {"nike": "M", "adidas": "46"},
#                 "L": {"nike": "L", "adidas": "48"},
#             }
#         },
#         "female": {
#             "nike": {
#                 "S": {"adidas": "36", "zara": "S"},
#                 "M": {"adidas": "38", "zara": "M"},
#                 "L": {"adidas": "40", "zara": "L"},
#             },
#             "adidas": {
#                 "36": {"nike": "S", "zara": "S"},
#                 "38": {"nike": "M", "zara": "M"},
#                 "40": {"nike": "L", "zara": "L"},
#             },
#             "zara": {
#                 "S": {"nike": "S", "adidas": "36"},
#                 "M": {"nike": "M", "adidas": "38"},
#                 "L": {"nike": "L", "adidas": "40"},
#             }
#         }
#     },

#     # =======================
#     # PANTS
#     # =======================
#     "pants": {
#         "male": {
#             "nike": {
#                 "32": {"adidas": "32", "zara": "32"},
#                 "34": {"adidas": "34", "zara": "34"},
#                 "36": {"adidas": "36", "zara": "36"},
#             },
#             "adidas": {
#                 "32": {"nike": "32", "zara": "32"},
#                 "34": {"nike": "34", "zara": "34"},
#                 "36": {"nike": "36", "zara": "36"},
#             },
#             "zara": {
#                 "32": {"nike": "32", "adidas": "32"},
#                 "34": {"nike": "34", "adidas": "34"},
#                 "36": {"nike": "36", "adidas": "36"},
#             }
#         },
#         "female": {
#             "nike": {
#                 "26": {"adidas": "34", "zara": "34"},
#                 "28": {"adidas": "36", "zara": "36"},
#                 "30": {"adidas": "38", "zara": "38"},
#             },
#             "adidas": {
#                 "34": {"nike": "26", "zara": "34"},
#                 "36": {"nike": "28", "zara": "36"},
#                 "38": {"nike": "30", "zara": "38"},
#             },
#             "zara": {
#                 "34": {"nike": "26", "adidas": "34"},
#                 "36": {"nike": "28", "adidas": "36"},
#                 "38": {"nike": "30", "adidas": "38"},
#             }
#         }
#     },

#     # =======================
#     # JACKETS
#     # =======================
#     "jackets": {
#         "male": {
#             "nike": {
#                 "S": {"adidas": "44", "zara": "S"},
#                 "M": {"adidas": "46", "zara": "M"},
#                 "L": {"adidas": "48", "zara": "L"},
#             },
#             "adidas": {
#                 "44": {"nike": "S", "zara": "S"},
#                 "46": {"nike": "M", "zara": "M"},
#                 "48": {"nike": "L", "zara": "L"},
#             },
#             "zara": {
#                 "S": {"nike": "S", "adidas": "44"},
#                 "M": {"nike": "M", "adidas": "46"},
#                 "L": {"nike": "L", "adidas": "48"},
#             }
#         },
#         "female": {
#             "nike": {
#                 "S": {"adidas": "36", "zara": "S"},
#                 "M": {"adidas": "38", "zara": "M"},
#                 "L": {"adidas": "40", "zara": "L"},
#             },
#             "adidas": {
#                 "36": {"nike": "S", "zara": "S"},
#                 "38": {"nike": "M", "zara": "M"},
#                 "40": {"nike": "L", "zara": "L"},
#             },
#             "zara": {
#                 "S": {"nike": "S", "adidas": "36"},
#                 "M": {"nike": "M", "adidas": "38"},
#                 "L": {"nike": "L", "adidas": "40"},
#             }
#         }
#     },

#     # =======================
#     # SHOES
#     # =======================
#     "shoes": {
#         "male": {
#             "nike": {
#                 "8": {"adidas": "42", "zara": "42"},
#                 "9": {"adidas": "43", "zara": "43"},
#                 "10": {"adidas": "44", "zara": "44"},
#             },
#             "adidas": {
#                 "42": {"nike": "8", "zara": "42"},
#                 "43": {"nike": "9", "zara": "43"},
#                 "44": {"nike": "10", "zara": "44"},
#             },
#             "zara": {
#                 "42": {"nike": "8", "adidas": "42"},
#                 "43": {"nike": "9", "adidas": "43"},
#                 "44": {"nike": "10", "adidas": "44"},
#             }
#         },
#         "female": {
#             "nike": {
#                 "6": {"adidas": "38", "zara": "38"},
#                 "7": {"adidas": "39", "zara": "39"},
#                 "8": {"adidas": "40", "zara": "40"},
#             },
#             "adidas": {
#                 "38": {"nike": "6", "zara": "38"},
#                 "39": {"nike": "7", "zara": "39"},
#                 "40": {"nike": "8", "zara": "40"},
#             },
#             "zara": {
#                 "38": {"nike": "6", "adidas": "38"},
#                 "39": {"nike": "7", "adidas": "39"},
#                 "40": {"nike": "8", "adidas": "40"},
#             }
#         }
#     }
# }

# # --------------------------------------------------
# # CATEGORY-AWARE LOOKUP FUNCTION (With Logging)
# # --------------------------------------------------

# def get_mapped_size_by_category(
#     category,
#     gender,
#     from_brand,
#     from_size,
#     to_brand
# ):
#     """Retrieves the mapped size based on brand, category, and gender"""
#     try:
#         # Normalize inputs to match dictionary keys
#         result = CATEGORY_SIZE_MAP[
#             category
#         ][
#             gender
#         ][
#             from_brand.lower()
#         ][
#             str(from_size)
#         ][
#             to_brand.lower()
#         ]
        
#         logger.info(f"Mapping Success: {from_brand} {from_size} -> {to_brand} {result} ({category}/{gender})")
#         return result

#     except KeyError as e:
#         logger.warning(f"Mapping Failed: {from_brand} {from_size} -> {to_brand} ({category}/{gender}). Error Key: {e}")
#         return None

# # --------------------------------------------------
# # [NEW] HELPER FOR DROPDOWN
# # --------------------------------------------------
# def get_supported_sizes(category, gender, brand):
#     """Returns a list of valid sizes for the dropdown based on inputs."""
#     try:
#         # Example: returns ['S', 'M', 'L'] or ['44', '46', '48']
#         return list(CATEGORY_SIZE_MAP[category][gender][brand.lower()].keys())
#     except KeyError:
#         return ["M"] # Fallback default

# mapping.py
from logger import get_logger

logger = get_logger("VTO-Mapping")

# ==================================================
# SIZE MAPPING FOR VIRTUAL TRY-ON
# Categories: tshirts, pants, jackets, shoes
# Brands: nike, adidas, zara
# ==================================================

CATEGORY_SIZE_MAP = {

    # =======================
    # T-SHIRTS
    # =======================
    "tshirts": {
        "male": {
            "nike": {
                "S": {"adidas": "44", "zara": "S"},
                "M": {"adidas": "46", "zara": "M"},
                "L": {"adidas": "48", "zara": "L"},
            },
            "adidas": {
                "44": {"nike": "S", "zara": "S"},
                "46": {"nike": "M", "zara": "M"},
                "48": {"nike": "L", "zara": "L"},
            },
            "zara": {
                "S": {"nike": "S", "adidas": "44"},
                "M": {"nike": "M", "adidas": "46"},
                "L": {"nike": "L", "adidas": "48"},
            }
        },
        "female": {
            "nike": {
                "S": {"adidas": "36", "zara": "S"},
                "M": {"adidas": "38", "zara": "M"},
                "L": {"adidas": "40", "zara": "L"},
            },
            "adidas": {
                "36": {"nike": "S", "zara": "S"},
                "38": {"nike": "M", "zara": "M"},
                "40": {"nike": "L", "zara": "L"},
            },
            "zara": {
                "S": {"nike": "S", "adidas": "36"},
                "M": {"nike": "M", "adidas": "38"},
                "L": {"nike": "L", "adidas": "40"},
            }
        }
    },

    # =======================
    # PANTS
    # =======================
    "pants": {
        "male": {
            "nike": {
                "32": {"adidas": "32", "zara": "32"},
                "34": {"adidas": "34", "zara": "34"},
                "36": {"adidas": "36", "zara": "36"},
            },
            "adidas": {
                "32": {"nike": "32", "zara": "32"},
                "34": {"nike": "34", "zara": "34"},
                "36": {"nike": "36", "zara": "36"},
            },
            "zara": {
                "32": {"nike": "32", "adidas": "32"},
                "34": {"nike": "34", "adidas": "34"},
                "36": {"nike": "36", "adidas": "36"},
            }
        },
        "female": {
            "nike": {
                "26": {"adidas": "34", "zara": "34"},
                "28": {"adidas": "36", "zara": "36"},
                "30": {"adidas": "38", "zara": "38"},
            },
            "adidas": {
                "34": {"nike": "26", "zara": "34"},
                "36": {"nike": "28", "zara": "36"},
                "38": {"nike": "30", "zara": "38"},
            },
            "zara": {
                "34": {"nike": "26", "adidas": "34"},
                "36": {"nike": "28", "adidas": "36"},
                "38": {"nike": "30", "adidas": "38"},
            }
        }
    },

    # =======================
    # JACKETS
    # =======================
    "jackets": {
        "male": {
            "nike": {
                "S": {"adidas": "44", "zara": "S"},
                "M": {"adidas": "46", "zara": "M"},
                "L": {"adidas": "48", "zara": "L"},
            },
            "adidas": {
                "44": {"nike": "S", "zara": "S"},
                "46": {"nike": "M", "zara": "M"},
                "48": {"nike": "L", "zara": "L"},
            },
            "zara": {
                "S": {"nike": "S", "adidas": "44"},
                "M": {"nike": "M", "adidas": "46"},
                "L": {"nike": "L", "adidas": "48"},
            }
        },
        "female": {
            "nike": {
                "S": {"adidas": "36", "zara": "S"},
                "M": {"adidas": "38", "zara": "M"},
                "L": {"adidas": "40", "zara": "L"},
            },
            "adidas": {
                "36": {"nike": "S", "zara": "S"},
                "38": {"nike": "M", "zara": "M"},
                "40": {"nike": "L", "zara": "L"},
            },
            "zara": {
                "S": {"nike": "S", "adidas": "36"},
                "M": {"nike": "M", "adidas": "38"},
                "L": {"nike": "L", "adidas": "40"},
            }
        }
    },

    # =======================
    # SHOES
    # =======================
    "shoes": {
        "male": {
            "nike": {
                "8": {"adidas": "42", "zara": "42"},
                "9": {"adidas": "43", "zara": "43"},
                "10": {"adidas": "44", "zara": "44"},
            },
            "adidas": {
                "42": {"nike": "8", "zara": "42"},
                "43": {"nike": "9", "zara": "43"},
                "44": {"nike": "10", "zara": "44"},
            },
            "zara": {
                "42": {"nike": "8", "adidas": "42"},
                "43": {"nike": "9", "adidas": "43"},
                "44": {"nike": "10", "adidas": "44"},
            }
        },
        "female": {
            "nike": {
                "6": {"adidas": "38", "zara": "38"},
                "7": {"adidas": "39", "zara": "39"},
                "8": {"adidas": "40", "zara": "40"},
            },
            "adidas": {
                "38": {"nike": "6", "zara": "38"},
                "39": {"nike": "7", "zara": "39"},
                "40": {"nike": "8", "zara": "40"},
            },
            "zara": {
                "38": {"nike": "6", "adidas": "38"},
                "39": {"nike": "7", "adidas": "39"},
                "40": {"nike": "8", "adidas": "40"},
            }
        }
    }
}


def get_mapped_size_by_category(category, gender, from_brand, from_size, to_brand):
    """Retrieves the mapped size based on brand, category, and gender."""
    try:
        result = CATEGORY_SIZE_MAP[category][gender][from_brand.lower()][str(from_size)][to_brand.lower()]
        logger.info(f"Mapping Success: {from_brand} {from_size} -> {to_brand} {result} ({category}/{gender})")
        return result
    except KeyError as e:
        logger.warning(f"Mapping Failed: {from_brand} {from_size} -> {to_brand} ({category}/{gender}). Missing Key: {e}")
        return None


def get_supported_sizes(category, gender, brand):
    """Returns a list of valid sizes for the dropdown based on inputs."""
    try:
        return list(CATEGORY_SIZE_MAP[category][gender][brand.lower()].keys())
    except KeyError:
        return ["M"]  # Fallback default