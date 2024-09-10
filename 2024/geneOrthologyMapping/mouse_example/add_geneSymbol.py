"""

Input:
- human_to_mouse_mapping.tsv: A tab-separated file containing the human-to-mouse
  GeneID mapping.
- gene2accession_human-mouse: The gene2accession file that contains the gene symbols.

Output:
- human_mouse_symbols_mapping.tsv: A tab-separated file containing the final 
  mapping of GeneIDs and symbols for both human and mouse genes.

USAGE: python sys.argv[0] 
"""


import pandas as pd

# Step 1: Load the human-to-mouse mapping
mapping_df = pd.read_csv("human_to_mouse_mapping.tsv", sep="\t")

# Step 2: Initialize dictionaries to hold gene symbols
human_symbols = {}
mouse_symbols = {}

# Step 3: Parse the large gene2accession file to fill the dictionaries
with open("gene2accession_human-mouse", "r") as f:  # Adjust the path to your gene2accession file
    for line in f:
        if line.startswith("#"):
            continue  # Skip header lines
        fields = line.strip().split("\t")
        gene_id = fields[1]
        symbol = fields[-1]

        # Populate the dictionaries
        if gene_id in mapping_df['Human_GeneID'].astype(str).values:
            human_symbols[gene_id] = symbol
        if gene_id in mapping_df['Mouse_GeneID'].astype(str).values:
            mouse_symbols[gene_id] = symbol

# Step 4: Create a DataFrame to store the final mapping with symbols
final_mapping = []
for index, row in mapping_df.iterrows():
    human_gene_id = str(row['Human_GeneID'])
    mouse_gene_id = str(row['Mouse_GeneID'])
    
    human_symbol = human_symbols.get(human_gene_id, "NA")
    mouse_symbol = mouse_symbols.get(mouse_gene_id, "NA")
    
    final_mapping.append([human_gene_id, human_symbol, mouse_gene_id, mouse_symbol])

final_mapping_df = pd.DataFrame(final_mapping, columns=["Human_GeneID", "Human_Symbol", "Mouse_GeneID", "Mouse_Symbol"])

# Step 5: Save the final result to a file
final_mapping_df.to_csv("human_mouse_symbols_mapping.tsv", sep='\t', index=False)
