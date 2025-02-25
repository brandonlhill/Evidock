import os
import sys
import json
import subprocess

def run_cmd(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def analyze_file(filepath):
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}"}

    results = {
        "filename": os.path.basename(filepath),
        "sha256": run_cmd(f"sha256sum {filepath} | awk '{{print $1}}'"),
        "file_type": run_cmd(f"file {filepath}"),
        "binwalk": run_cmd(f"binwalk {filepath}"),
        "exiftool": run_cmd(f"exiftool {filepath}")
    }

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file provided"}))
        sys.exit(1)

    file_path = sys.argv[1]
    analysis_results = analyze_file(file_path)

    # Print valid JSON so the host script can capture it
    print(json.dumps(analysis_results, indent=4))
