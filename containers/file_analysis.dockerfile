FROM debian:latest

# Install necessary tools
RUN apt-get update && apt-get install -y \
    file binwalk exiftool coreutils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /analyze

# Copy the Python script into the container (Make sure filename is correct!)
COPY file_analysis.py /analyze/analyze.py

# Set the script as the default entrypoint
ENTRYPOINT ["python3", "/analyze/analyze.py"]
