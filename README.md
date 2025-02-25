# Evidock
EviDock is a Docker-based toolchain designed to automate the analysis of ingested files while seamlessly integrating human-driven investigation. It streamlines forensic workflows by extracting, processing, and structuring artifacts—the digital evidence produced during analysis.

By leveraging containerized automation, EviDock efficiently identifies, classifies, and logs findings from PCAPs, binaries, documents, and more, reducing manual effort while ensuring that human analysts can interact with, interpret, and refine the generated artifacts.

# Build Instructions

Please make sure docker is installed (also not that we are using the old 'docker build' system for now. 

The following commands below will build the file_analysis container and generate a file report in artifacts for /bin/ls  
```bash
make containers/build

sudo python3 run_analysis.py /bin/ls

cat artifacts/*

```
