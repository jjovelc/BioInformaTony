# Extract Entrez IDs.
# File mmusculus_transcript_attributes_240908.stv was create with script retrieve_biomaRt_annotations.R
sed 1d mmusculus_transcript_attributes_240908.tsv | cut -f 4 | grep -v "NA" | sort | uniq > mmusculus_genelist.txt

# Prepare a human-mouse gene2accession file
grep -w "^9606\|10090^" gene2accession > gene2accession_human-mouse

# Retrieve human orthologues
datasets download gene gene-id --inputfile mmusculus_genelist.txt --ortholog 9606 --filename mouse-human_orthologs.zip

# Decompress mouse-human_orthologs.zip
unzip mouse-human_orthologs.zip

# Parse ncbi_dataset/data/data_report.jsonl file containing the human orthologues.
python parse_jsonl.py

This will produce file ncbi_dataset/data/extracted_human_gene_ids.txt 

# Pair the extracted human orthologs gene IDs with the corresponding mouse gene IDs
python find_mouse_orthologues.py

# map the retrieved human Entrez gene IDs to their mouse cognates find_mouse_orthologs.py
python add_geneSymbol.py

# Count records for genes symbols that are identical between the two organisms
awk '$2 == $4' human_mouse_symbols_mapping.tsv | wc -l

# Count records for genes symbols that are different between the two organisms, do:
awk '$2 != $4' human_mouse_symbols_mapping.tsv | wc -l



