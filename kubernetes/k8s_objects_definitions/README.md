# Kubernetes Object Definitions Exporter

This folder contains Markdown files with the definitions of all available Kubernetes API resources (Objects) in your cluster.

## Files Structure
Each file follows the naming convention `[api_resource_name].md` (e.g., `pods.md`, `services.md`).
The content is generated using `kubectl explain [resource] --recursive` and is formatted for easy reading:
- **Header**: Contains the Kind and API Version.
- **Body**: The explanation is wrapped in a YAML code block for syntax highlighting.

## How to Refresh/Update Definitions

A Python script `fetch_k8s_definitions.py` is included to regenerate these files. Use this if you upgrade your cluster or want to refresh the documentation.

### Prerequisites
- **Python 3** installed.
- **kubectl** installed and configured with access to your cluster.

### Usage
Run the script from inside this directory:

```bash
python3 fetch_k8s_definitions.py
```

The script will:
1. Fetch all available API resources from your cluster.
2. Run `kubectl explain` for each one.
3. Overwrite the existing `.md` files in this directory.
