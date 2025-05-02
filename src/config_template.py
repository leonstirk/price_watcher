import os

####################################################################################################
# Email Alert Settings (AWS SES)
####################################################################################################

SENDER = os.getenv("SES_SENDER", "your-sender@example.com")
RECIPIENT = os.getenv("SES_RECIPIENT", "your-recipient@example.com")
REGION = os.getenv("AWS_REGION", "ap-southeast-2")  # e.g. "us-east-1"

####################################################################################################
# Store Location IDs (New World store identifiers)
####################################################################################################

STORE_IDS = {
    "Dunedin": "store-id-here",
    "Chaffers": "store-id-here"
    # Add more stores as needed
}

def get_store_ids(store_name: str) -> tuple[str, str]:
    """
    Given a store name, return the STORE_ID_V2 and eCom_STORE_ID pair.

    STORE_ID_V2 format is: "{store_id}|False"
    eCom_STORE_ID format is: "{store_id}"
    """
    if store_name not in STORE_IDS:
        raise ValueError(f"Store '{store_name}' not found in store list.")
    store_id = STORE_IDS[store_name]
    return f"{store_id}|False", store_id
