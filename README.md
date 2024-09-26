# `biobalm` reproducibility artefact

This archive contains all the code and data necessary to reproduce the results presented in the 
"Mapping the attractor landscape of Boolean networks" paper.

### Artefact structure

 * `models-generator`: Scripts used to generate random models. You don't have to use these, the generated models are already included. These are just for completeness.
 * `models`: Model files that are used during testing of `biobalm`.
 * `benchmark-attractor`: Scripts necessary for reproducing the attractor detection comparison between `biobalm`, `aeon`, and `mts-nfvs`, including out measured data.
 * `benchmark-construction`: Comparison of full succession diagram construction between `biobalm` and `pystablemotifs`.
 * `benchmark-control`: Comparison of target control between `biobalm` and `pystablemotifs`.
 * `analysis`: Python scripts and notebooks that were used to generate the figures presented in the paper.

Every part of the artefact has a dedicated README file which should instruct you on how to reproduce the analysis.