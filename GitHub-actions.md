### Changed-Files

Changed-Files action allows conditional execution of workflow steps and jobs, based on the modified files.

You can run slow tasks like integration tests or deployments only for changed components. It saves time and resources, especially in monorepo setups.

GitHub workflows built-in path filters don't work on a level of individual jobs or steps.

#### Example:

The example below demonstrates how changed-files action can be used on the workflow jobs level.

The workflow below will run on successful completion of dnsmasq-deploy workflow. The workflow will first run changes-detection job which will detect changes to files inside the {{ env.SERVICES_OFFICE_PRAGUE_DIR }} and {{ env.CONFIGS_DIR }} directories.  If any files have changed since the last commit (changes-detection.outputs.healthchecks returned true), the next job deploy-healthchecks will be executed.

```
name: deploy-office-prague

on:
  workflow_run:
    workflows:
      - dnsmasq-deploy
    branches:
      - main
    types:
      - completed
env:
  SERVICES_OFFICE_PRAGUE_DIR: "clusters/office-prague"
  CONFIGS_DIR: "config"

jobs:
  changes-detection:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-20.04
    outputs:
      healthchecks: ${{ steps.healthchecks.outputs.any_changed }}
    steps:
      - uses: actions/checkout@v3
      - name: get-changed-files-healthchecks
        uses: tj-actions/changed-files@v33
        id: healthchecks
        with:
          files: |
             {{ env.SERVICES_OFFICE_PRAGUE_DIR }}/**
             {{ env.CONFIGS_DIR }}: "config"/**

  deploy-healthchecks:
    needs: changes-detection
    if: ${{ needs.changes-detection.outputs.healthchecks == 'true' }}
    runs-on: ubuntu-20.04
    steps:
      - run: echo "run something..."
```
