# Load the biomaRt package
library(biomaRt)
listMarts()
setwd('') # Include your directory here
rm(list=ls())

ensembl=useMart("ensembl")
listDatasets(ensembl)

# Set the dataset to use
species <- "ecaballus"
mart <- useMart("ensembl", dataset = paste0(species, "_gene_ensembl")


outfile <- paste0(species, "_transcript_attributes_240827.tsv"

# Set the attributes to retrieve
# Make list of attributes to retrieve
attributes <- c("ensembl_transcript_id",
                "ensembl_gene_id",
                "external_gene_name",
                "entrezgene_id",
                "wikigene_description",
                "name_1006",
                "definition_1006",
                "namespace_1003")

# Get the transcripts and their attributes
transcripts_annotations <- getBM(attributes = attributes,
                     mart = mart)

# Write the results to a tsv file
write.table(transcripts_annotations, file = outfile, sep = "\t", quote = FALSE, row.names = FALSE)
