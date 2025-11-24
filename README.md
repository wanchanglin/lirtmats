# LiRTMaTS - Liverpool Retention Time Matching Software 

## Introduction

Untargeted metabolomics studies routinely apply liquid chromatography-mass
spectrometry (LC-MS) to acquire data for hundreds or low thousands of
metabolites and exposome-related (bio)chemicals. The annotation or
higher-confidence identification of metabolites and biochemicals can apply
multiple different data types (1) chromatographic retention time, (2) the
mass-to-charge (m/z) ratio of ions formed during electrospray ionisation for
the structurally intact metabolite or (bio)chemical and (3) fragmentation
mass spectra derived from MS/MS or MSn experiments.

Chromatographic retention time is a complementary data type when compared to
m/z and MS/MS data. Method-specific retention time (RT) libraries can be
constructed by the analysis of pure metabolite standards applying the same
assay and reporting the detected RT. The library RT can be compared to RT of
a metabolite detected in an untargeted metabolomics study to aid in the
annotation or identification of metabolites. The `LiRTMaTS` is a Python
package and easy-to-use software for matching RTs detected in an untargeted
metabolomics study to RTs present in a RT library. Any RT library can be
applied though this RT library should be specific to the LC-MS assay applied
(RT libraries are not transferable across different LC-MS assays). All
matches within a RT range are reported.

## Authors

- Wanchang Lin (<Wanchang.Lin@liverpool.ac.uk>), The University of Liverpool
- Warwick Dunn (<Warwick.Dunn@liverpool.ac.uk>), The University of Liverpool

