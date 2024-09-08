"""
Description:
This script processes a gene ortholog file to identify human-to-horse orthologs
based on a provided list of human gene IDs. It specifically filters for orthologs
related to horses (taxonomy ID 9796) and generates a mapping between human 
and horse GeneIDs.

Input:
- gene_orthologs: A tab-separated file containing ortholog information for multiple
  species.
- extracted_human_gene_ids.txt: A text file containing human GeneIDs to be filtered.

Output:
- human_to_horse_mapping.tsv: A tab-separated file containing the final mapping 
  of human and horse GeneIDs.

USAGE: python sys.argv[0]
"""

import pandas as pd

# Load the gene orthologs file
gene_orthologs = pd.read_csv("gene_orthologs", sep="\t")

infile="ncbi_dataset/data/extracted_human_gene_ids.txt"

# Load the list of human gene IDs from the extracted_human_gene_ids.txt file
with open(infile, "r") as file:
    human_gene_ids = [line.strip() for line in file]

# Convert human_gene_ids to integers if the GeneID in gene_orthologs is an integer
human_gene_ids = list(map(int, human_gene_ids))

# Filter the dataframe to find orthologs in horses (taxonomy ID 9796)
horse_human_orthologs = gene_orthologs[(gene_orthologs['GeneID'].isin(human_gene_ids)) & 
                                       (gene_orthologs['Other_tax_id'] == 9796)]

# Extract the relevant columns: human GeneID and horse GeneID
human_to_horse_mapping = horse_human_orthologs[['GeneID', 'Other_GeneID']]

# Rename columns for clarity
human_to_horse_mapping.columns = ['Human_GeneID', 'Horse_GeneID']

# Display the mapping
print(human_to_horse_mapping.head())

# Optionally, save the mapping to a file
# Change the name of this output file if needed
human_to_horse_mapping.to_csv("human_to_horse_mapping.tsv", index=False, sep="\t")
