Below are the steps to follow to reproduce the pipeline presented in the video.

1. Get annotations for the organism of interest, in this case Equus caballus (using script retrieve_biomaRt_annotations.R). 
- First four columns of resulting table will look like this:

| ensembl_transcript_id	| ensembl_gene_id	   | external_gene_name	| entrezgene_id|	
|-----------------------|--------------------|--------------------|--------------|
| ENSECAT00000029856    | ENSECAG00000027684 | MT-ND1	            | 807846       |	
| ENSECAT00000126620    | ENSECAG00000024263 | PRKRA	            | 100067259    |

- Since the Entrez ID is in column 4, to extract the Entrez ids, use the following command:

```bash
sed 1d ecaballus_transcript_attributes_240908.tsv | cut -f 4 | grep -v "NA" | sort | uniq > horse_genelist.txt 	
```

1. Download NCBI datasets from the following link: https://ftp.ncbi.nih.gov/gene/DATA/

- Download files: gene_orthologs.gz and gene2accession.gz 
- Decompress downloaded files
- Extract from file gene2accession only the taxa needed, in this case horse (9796) and human (9606):

```bash
grep -w "^9606\|^9796" gene2accession > gene2accession_human-horse
```

3. Create a conda environment for the NCBI DATASETS (https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/):

```bash
	conda create -n ncbi_datasets
	conda activate ncbi_datasets
	conda install -c conda-forge ncbi-datasets-cli # This install the commnand-line interface
```	
	 
4. Use the NCBI command line interface to look for human orthologs of the horse genes, with the following command:

```bash
conda activate ncbi_datasets
datasets download gene gene-id --inputfile horse_genelist.txt --ortholog 9606 --filename horse_human_orthologs.zip
```

Decompress file: horse_human_orthologs.zip

This will contain the following structure:<br>
-ncbi_dataset/data/<br>
|<br>
|-data_report.jsonl  dataset_catalog.json  extracted_human_gene_ids.txt  parse_jsonl.py  protein.faa  rna.fna<br>

5. Use script find_horse_orthologs.py to pair the extracted human orthologs gene IDs with the corresponding horse gene IDs using as input files ncbi_dataset/data/extracted_human_gene_ids.txt and gene_orthologs. This will generate output file human_to_horse_mapping.tsv.

```bash
python find_horse_orthologs.py
```

6. Use script add_geneSymbol.py to add a gene symbol to the Entrez IDs. This script will use human_to_horse_mapping.tsv and gene2accession_human-horse as input and will produce the file with the final results: human_horse_symbols_mapping.tsv containing the mapping of orthologs. Such file will look like:

```bash
python add_geneSymbol.py
```

|Human_GeneID	| Human_Symbol |	Horse_GeneID	| Horse_Symbol |
|-------------|--------------|----------------|--------------| 
| 1           |	A1BG	       | 100064369	    | A1BG         |
| 2	          | A2M	         | 100061692	    | A2M          |
| 14	        | AAMP	       | 100058415	    | AAMP         |
| 15	        | AANAT	       | 100058770	    | AANAT        |
| 16	        | AARS1	       | 100054983	    | AARS1        |
| 18	        | ABAT	       | 100051470	    | ABAT         |
| 19	        | ABCA1	       | 100054241	    | ABCA1        |
| 20	        | ABCA2	       | 100067889	    | ABCA2        |
| 21	        | ABCA3	       | 100068313	    | ABCA3        |


- If you want to extract records for genes symbols that are identical between the two organisms, do:

```bash
awk '$2 == $4' human_horse_symbols_mapping.tsv
```

- If you want to extract records for genes symbols that are different between the two organisms, do:

```bash
awk '$2 != $4' human_horse_symbols_mapping.tsv
```