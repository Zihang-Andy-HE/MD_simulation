# GROMACS version: gromacs-2024.3
# PDB file: 1yrt.pdb
# Remove unwanted water
grep -v HOH 1yrt.pdb > 1YRT_clean.pdb
# Generate topology file, position restraint file and the post-processed structure file
gmx pdb2gmx -f 1YRT_clean.pdb -o 1YRT_processed.gro -water spce -ignh # 6
# 6: AMBER99SB-ILDN protein, nucleic AMBER94 (Lindorff-Larsen et al., Proteins 78, 1950-58, 2010)
# Define the box; Produce topol.top
gmx editconf -f 1YRT_processed.gro -o 1YRT_box.gro -c -d 1.0 -bt cubic
# Fill it with solvent (water)
gmx solvate -cp 1YRT_box.gro -cs spc216.gro -o 1YRT_solv.gro -p topol.top
# Add ions (Na+ and Cl-) 0.15M represent human physiological salinity
gmx grompp -f ions.mdp -c 1YRT_solv.gro -p topol.top -o ions.tpr -maxwarn 3
gmx genion -s ions.tpr -o 1YRT_ionized.gro -p topol.top -pname NA -nname CL -neutral -conc 0.15
# Minimize the energy
gmx grompp -f minim.mdp -c 1YRT_ionized.gro -p topol.top -o em.tpr -maxwarn 1
# Run MD
gmx mdrun -v -deffnm em # -ntomp 8
# Energy analysis: Energy potential should be in the range  -10e5:-10e6
gmx energy -f em.edr -o potential.xvg # 10 0
# NVT equilibration
gmx grompp -f nvt_short.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt -ntomp 8
# Analysis of the temperature progression, using energy
gmx energy -f nvt.edr -o temperature.xvg # 16 0
# NPT equilibration
gmx grompp -f npt_short.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt
# Analysis of the pressure progression, using energy
gmx energy -f npt.edr -o pressure.xvg # 18 0
# Analysis of density progression, using energy
gmx energy -f npt.edr -o density.xvg # 24 0
# MD production; Temperature changed in md_short.mdp as 280K, 300K and 320K; time set as 50ns
gmx grompp -f md_short.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_300.tpr
# Run MD: cost several hours or even days
gmx mdrun -deffnm md_0_300 -cpi md_0_300.cpt -nb gpu
# Remove PBC
gmx trjconv -s md_0_300.tpr -f md_0_300.xtc -o md_0_300_noPBC.xtc -pbc mol -center # 1 0
# RMSD Structural stability analysis. Relative to the structure present in the minimized, equilibrated system. 
gmx rms -s md_0_300.tpr -f md_0_300_noPBC.xtc -o rmsd_300.xvg -tu ns # 4 0
# RMSD Structural stability analysis. Relative to the crystal structure.
gmx rms -s em.tpr -f md_0_300_noPBC.xtc -o rmsd_300_xtal.xvg -tu ns # 4 0
# Gyration analysis
gmx gyrate -s md_0_300.tpr -f md_0_300_noPBC.xtc -o gyrate_300.xvg # 1
# Extract the PDB from trajectory at 50 ns
gmx trjconv -s md_0_300.tpr -f md_0_300_noPBC.xtc -o md_0_300_trj_50.pdb -dump 50000 # 0


# DSSP Secondary structure analysis
gmx dssp -f md_0_300_noPBC.xtc -s md_0_300.tpr -num dssp_300.xvg # 1
# Ramachandran plot
# codes from https://github.com/gerdos/PyRAMA

# PDBePISA
# https://www.ebi.ac.uk/msd-srv/prot_int/pistart.html

# AlphaFold3 FASTA file from PDB: 1yrt.pdb
# https://alphafoldserver.com/

# # PyMol
# cmd.remove("solvent")
# remove resn CL
# remove resn NA or resn SOD
# split_chains
# # Select the pocket region
# create pocket, sele
# cmd.show("sticks"    ,"pocket")
# util.cba(154,"pocket",_self=cmd)
# ray
# png 1YRT_pocket.png, 16.93cm, 16.93cm, dpi=300

# # Line plot (time as x axis)
# RMSD, Rg # 320K red, 300K green, 280K blue
# Secondary Structure Dynamics # y axis - residue count; α-Helices: #E63946, β-Strands: #1D3557; β-Bridges: #2A9D8F

# # Violin plots 5 conditions
# GROMACS simulation pick 5 time points as replicates (30ns, 35ns, 40ns, 45ns, 50ns) in three temperature condition 280K, 300K, 320K
# AlphaFold3 for WT and W242G 5 outputs as replicates
