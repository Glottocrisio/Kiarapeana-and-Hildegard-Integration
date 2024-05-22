import os

# List of repository directories
repos = [
    "kiara",
    "kiara_plugin.network_analysis",
    "NetworkAnalysis",
    "TopicModelling-",
    "jupyterlab-extension-example",
    "asciinet"
]

# Output file
output_file = "DHARPA_Project_code.txt"

with open(output_file, 'w', encoding='utf-8') as outfile:
    for repo in repos:
        for root, _, files in os.walk(repo):
            for file in files:
                file_path = os.path.join(root, file)
                # Specify file extensions you want to include
                if file.endswith(('.py', '.md', '.txt', '.sh', '.json', '.js', '.yml', '.yaml', '.html', '.css', '.ts', '.jsx', '.tsx')):
                    outfile.write(f"\n\n# {file_path}\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"Could not read file {file_path}: {e}\n")
