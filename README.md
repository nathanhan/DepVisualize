# nahanmodule

## Requirements
- baseruntime-package-lists download_repo.sh to mirror rpm directory locally and generate Fedora-26-Beta-repos.cfg file
- Copy of Fedora-26-Beta-repos.cfg in nahanmodule directory
- depchase verbose branch installed as a command
- python3-modulemd
- python3-pydot
- python3-argparse
- Recommended to have base-runtime, shared-userspace, and common-build-dependencies modulemd files in nahanmodule/yamls/ directory
- Recommended to have execute permissions on every file in directory

## Example Usage
`./nahanmodule.py graphmany input.txt`