import os
import shutil
from kiara import Kiara
from pathlib import Path

# Set up test parameters
api_key = "YOUR_EUROPEANA_API_KEY"  # Replace with your Europeana API key
search_query = "science journals"
download_path = Path("./test_journals")

# Initialize Kiara
kiara = Kiara.instance()

# Define the module configuration
module_config = {
    "api_key": api_key,
    "search_query": search_query,
    "download_path": download_path,
}

# Run the module
module = kiara.create_manifest(module_or_operation="DownloadJournals", config=module_config)
kiara.process(module, inputs={})

# Validate the output
def validate_download(download_path):
    assert download_path.exists(), "Download path does not exist."
    assert len(list(download_path.glob("*.txt"))) > 0, "No journals were downloaded."

try:
    validate_download(download_path)
    print("Test passed: Journals were downloaded successfully.")
except AssertionError as e:
    print(f"Test failed: {e}")

# Clean up test environment
shutil.rmtree(download_path)

