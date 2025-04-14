# GROMACS Molecular Dynamics Simulation of CyaA-ACD/C-CaM Complex (PDB: 1YRT)

This repository contains scripts and configuration files for running molecular dynamics (MD) simulations of the CyaA-ACD/C-CaM complex (PDB ID: 1YRT) using GROMACS. The primary goal is to investigate the structural stability and interface interactions of the complex at different temperatures (280K, 300K, and 320K).

## Overview

The workflow involves:
1.  **System Preparation:** Cleaning the PDB file, generating topology using the AMBER99SB-ILDN force field, creating a simulation box, solvating with SPC/E water, and adding ions to physiological concentration (0.15 M NaCl).
2.  **Energy Minimization:** Removing steric clashes from the initial structure.
3.  **Equilibration:** Stabilizing the system temperature (NVT ensemble) and then pressure/density (NPT ensemble).
4.  **Production MD:** Running a 50 ns simulation at the target temperature (280K, 300K, or 320K).
5.  **Analysis:** Post-processing the trajectory to analyze structural stability (RMSD, Rg), secondary structure (DSSP), interface properties (PDBePISA), and comparing results with AlphaFold3 predictions (WT and W242G mutant).

## Requirements

*   **GROMACS:** Version 2024.3 or compatible.
*   **PDB File:** `1yrt.pdb`
*   **MDP Files:** Parameter files for GROMACS steps:
    *   `ions.mdp`
    *   `minim.mdp`
    *   `nvt_short.mdp`
    *   `npt_short.mdp`
    *   `md_short.mdp` (Temperature parameter `ref_t` needs to be set to 280, 300, or 320 for respective runs).
    *   *(These files should be present in the working directory)*
*   **Python:** For post-simulation analysis scripts (e.g., plotting, PyRAMA).
*   **PyRAMA:** (Optional, for Ramachandran plots) Installation required: `https://github.com/gerdos/PyRAMA`
*   **PyMOL:** (Optional, for visualization).
*   **Web Access:** For PDBePISA and AlphaFold3 submissions.
*   **Sufficient computing resources:** MD simulations, especially the production run, can be computationally intensive and require significant time (hours to days) and disk space. GPU acceleration is recommended (`-nb gpu`).
