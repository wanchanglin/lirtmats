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

## Installation

### Source

Install directly from GitHub: 

```bash
pip install git+https://github.com/wanchanglin/lirtmats.git
```

### PyPI (Coming soon)

To install from [PyPI](https://pypi.org/) via `pip`, use the distribution
name `lirtmats`:

```bash
pip install lirtmats
```

This is the preferred installation method.

Use the following to update if `lirtmats` has been installed before:

```bash
pip install lirtmats --upgrade    # upgrade to the newest version
```

### Conda (Coming soon)

`lirtmats` is in `Bioconda` channel and use the following to install or
update for conda:

```bash
conda install -c bioconda lirtmats
```

Use the following to update if `lirtmats` has been installed before:

```bash
conda update -c bioconda lirtmats       # upgrade to the newest version
```

## Usages

`lirtmats` provides command line and graphical user interfaces for the end
users.

    $ lirtmats --help
    Executing lirtmats version 1.0.0.
    usage: lirtmats [-h] {cli,gui} ...

    Retention Time Matching of LC-MS data

    positional arguments:
      {cli,gui}
        cli       Retention Time Matching in CLI.
        gui       Retention Time Matching in GUI.

    options:
      -h, --help  show this help message and exit

### Command line interface (CLI)

Use the follow command line to launch CLI mode: :

    $ lirtmats cli <arg_lists>

The following is an example:

    lirtmats cli \
      --input-data "./data/df_pos_3.tsv" \
      --input-sep "tab" \
      --col-idx "1, 2, 3, 4" \
      --rt-path "" \
      --rt-sep "tab" \
      --rt-tol "5.0" \
      --ion-mode "pos" \
      --save-db \
      --summ-type "xlsx" \

### Graphical user interface (GUI)

    $ lirtmats gui

## Links

- Documentation: [Read the Docs](https://lirtmats-liverpool-retention-time-matching-software.readthedocs.io/en/latest/)

## Authors

- Wanchang Lin (<Wanchang.Lin@liverpool.ac.uk>), The University of Liverpool
- Warwick Dunn (<Warwick.Dunn@liverpool.ac.uk>), The University of Liverpool

