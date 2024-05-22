import pyeuropeana as pye
import os

def download_journals(api_key, search_query, download_path):
    europeana = pye.(api_key)
    results = europeana.search(search_query)
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for item in results['items']:
        title = item['title'][0] if 'title' in item else 'unknown'
        data = europeana.get_item_data(item['id'])
        
        with open(os.path.join(download_path, f"{title}.txt"), 'w', encoding='utf-8') as file:
            file.write(data)
    print(download_path)
    return download_path


search_query = 'Belgium journals'
download_path = './belgian_journals'
download_journals('armendinguil', search_query, download_path)