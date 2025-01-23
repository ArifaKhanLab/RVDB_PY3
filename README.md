# RVDB_PY3
This is the repository of RVDB production scripts written by Python3 to replace the scripts in RVDB old repository which were  written by Python 2. Additionally, several improvements and refinements were implemented since the old release. 
#**Instructions for updating RVDB_PY3**

##**0.	Prerequisites**
RVDB Python3 (RVDB_PY3) scripts requires several third-party packages for data processing and most importantly, quality checking and clustering SARS-CoV-2 sequences. The prerequisites and their installation instructions are described as below.
###A.	Environment setup
We highly recommend to create an isolated Python3 environment by package managers such as Anaconda or Mamba. RVDB_PY3 was tested under the Python3 environment create by Mamba. The Mamba instruction is available at  https://github.com/mamba-org/mamba?tab=readme-ov-file.

###B.	Installation of prerequisites packages
We have provided a YAML Ain't Markup Language (YAML) file named “RVDB_PY3.YAML” which contains the setup instruction for RVDB_PY3 running under Mamba environment.  To create a mamba environment named “rvdb_pipeline” and install all prerequisites, please prompt:
`$ mamba env create -n rvdb_pipeline -f RVDB_PY3.yaml`

###C.	Environment activation
To activate “rvdb_pipeline” environment, please prompt:
`$ mamba activate rvdb_pipeline`

That’s it. You are ready to proceed to Step 1.
