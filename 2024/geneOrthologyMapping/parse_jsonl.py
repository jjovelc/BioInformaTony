import json

# Initialize a list to store human gene IDs
human_gene_ids = []

# Open and read the JSONL file
with open('data_report.jsonl', 'r') as file:
    for line in file:
        # Parse each line as a JSON object
        record = json.loads(line.strip())
        
        # Extract the human gene ID (geneId field) and add it to the list
        human_gene_id = record.get('geneId')
        if human_gene_id:
            human_gene_ids.append(human_gene_id)

# Display the extracted human gene IDs
print("Extracted Human Gene IDs:")
print(human_gene_ids)

# Optionally, save the list of human gene IDs to a file
with open('extracted_human_gene_ids.txt', 'w') as output_file:
    for gene_id in human_gene_ids:
        output_file.write(f"{gene_id}\n")
