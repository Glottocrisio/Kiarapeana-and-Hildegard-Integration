from kiara import KiaraModel
from pydantic import Field
from typing import Any, Dict
from pathlib import Path

class DownloadJournals(KiaraModel):
    api_key: str = Field(description="API key for accessing Europeana.")
    search_query: str = Field(description="Query string to search for journals.")
    download_path: Path = Field(description="Directory path where journals will be saved.", default=Path("./journals"))

    def run(self) -> Dict[str, Any]:
        download_path = self.download_journals(self.api_key, self.search_query, self.download_path)
        return {"download_path": download_path}

    def download_journals(self, api_key, search_query, download_path):
        from pyeuropeana import Europeana
        import os

        europeana = Europeana(api_key)
        results = europeana.search(search_query)
        
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        for item in results['items']:
            title = item['title'][0] if 'title' in item else 'unknown'
            data = europeana.get_item_data(item['id'])
            
            with open(os.path.join(download_path, f"{title}.txt"), 'w', encoding='utf-8') as file:
                file.write(data)

        return download_path

# Register the module with Kiara
from kiara import register_model
register_model(DownloadJournals)
