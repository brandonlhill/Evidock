import os
import json
import subprocess
import uuid
import argparse

# Directory to store artifacts
ARTIFACT_DIR = "./artifacts"

def ensure_artifact_dir():
    if not os.path.exists(ARTIFACT_DIR):
        os.makedirs(ARTIFACT_DIR)

def generate_artifact_filename(input_file):
    base_name = os.path.basename(input_file)
    return os.path.join(ARTIFACT_DIR, f"artifact_{base_name}.json")

def run_container(image_name, input_file):
    container_cmd = f"docker run --rm -v {os.getcwd()}:/data {image_name} /data/{input_file}"
    
    try:
        result = subprocess.run(container_cmd, shell=True, text=True, capture_output=True)
        raw_output = result.stdout.strip()
        
        print("\n[+] Raw Output from Docker Container:")
        print(raw_output)  # Print raw output for debugging
        
        return json.loads(raw_output)  # Attempt to parse JSON output
    except json.JSONDecodeError:
        print("\n[!] Error: Docker output is not valid JSON.")
        return {"error": "Invalid JSON output", "raw_output": raw_output}
    except Exception as e:
        return {"error": str(e)}

def append_to_artifact(artifact_file, data):
    try:
        if os.path.exists(artifact_file):
            with open(artifact_file, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = {}

        existing_data[str(uuid.uuid4())] = data  # Store each analysis with a unique key

        with open(artifact_file, "w") as f:
            json.dump(existing_data, f, indent=4)

        return existing_data
    except Exception as e:
        print(f"Error updating artifact file: {e}")
        return None

def main(input_file):
    ensure_artifact_dir()
    artifact_file = generate_artifact_filename(input_file)

    print(f"\n[+] Running file analysis on: {input_file}...\n")

    # Run Docker container for file analysis
    file_analysis = run_container("file_analysis", input_file)

    # Append results to artifact file
    updated_artifact = append_to_artifact(artifact_file, file_analysis)

    # Print the final artifact JSON
    print("\n[+] Final Artifact File Content:")
    print(json.dumps(updated_artifact, indent=4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate file analysis using Docker containers")
    parser.add_argument("input_file", help="Path to the file for analysis")
    args = parser.parse_args()

    main(args.input_file)
