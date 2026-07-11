import os
import subprocess
import re

OUTPUT_DIR = "."

def main():
    # Create directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    else:
        print(f"Directory {OUTPUT_DIR} already exists.")

    # Get list of all API resources
    print("Fetching list of API resources...")
    try:
        # Get names of resources
        result = subprocess.run(["kubectl", "api-resources", "--verbs=list", "-o", "name"], capture_output=True, text=True, check=True)
        resources = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error fetching api-resources: {e}")
        return

    print(f"Found {len(resources)} resources. Starting export...")

    success_count = 0
    
    for i, resource in enumerate(resources):
        if not resource: continue
        
        safe_name = resource.replace("/", "_") 
        filename = f"{OUTPUT_DIR}/{safe_name}.md"
        
        print(f"[{i+1}/{len(resources)}] Exporting {resource}...", end="", flush=True)
        
        try:
            # Run kubectl explain
            explain_proc = subprocess.run(
                ["kubectl", "explain", resource, "--recursive", "--output=plaintext-openapiv2"], 
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            content = explain_proc.stdout
            
            # Parse Kind and Version for the Header
            kind_match = re.search(r'^KIND:\s+(.+)$', content, re.MULTILINE)
            version_match = re.search(r'^VERSION:\s+(.+)$', content, re.MULTILINE)
            
            kind = kind_match.group(1).strip() if kind_match else resource
            version = version_match.group(1).strip() if version_match else "Unknown"

            # Write to Markdown file with formatting
            with open(filename, "w") as f:
                f.write(f"# Kind: {kind}\n")
                f.write(f"### Version: {version}\n\n")
                f.write("```yaml\n")
                f.write(content)
                if not content.endswith("\n"):
                    f.write("\n")
                f.write("```\n")
                
            print(" Done.")
            success_count += 1
            
        except subprocess.CalledProcessError:
            print(" Failed.")
        except subprocess.TimeoutExpired:
            print(" Timed out.")
        except Exception as e:
            print(f" Error: {e}")
    
    print(f"\nExport completed. Successfully exported {success_count} definitions to '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    main()
