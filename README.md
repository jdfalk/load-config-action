# Load Repository Config Action

Load and parse `.github/repository-config.yml` with fallback handling for GitHub Actions workflows.

## Features

- ✅ Loads YAML configuration files automatically
- ✅ Graceful fallback when config is missing (default: empty config)
- ✅ Parses YAML to JSON for downstream GitHub Actions
- ✅ Optional `fail-on-missing` to enforce config requirement
- ✅ Rich step summaries showing loaded config sections
- ✅ Automatic PyYAML installation if needed

## Usage

### Basic Example

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: jdfalk/load-config-action@v1
        id: config
        with:
          config-file: .github/repository-config.yml

      - name: Show config
        run: |
          echo "Has config: ${{ steps.config.outputs.has-config }}"
          echo "Config: ${{ steps.config.outputs.config }}"
```

### With Fail-On-Missing

```yaml
- uses: jdfalk/load-config-action@v1
  id: config
  with:
    config-file: .github/repository-config.yml
    fail-on-missing: true  # Workflow fails if config missing
```

### Using Config in Downstream Steps

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      config: ${{ steps.config.outputs.config }}
    steps:
      - uses: actions/checkout@v6
      - uses: jdfalk/load-config-action@v1
        id: config

  use-config:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - name: Process config
        env:
          REPO_CONFIG: ${{ needs.setup.outputs.config }}
        run: |
          echo "$REPO_CONFIG" | python -m json.tool
```

## Inputs

| Input             | Description                         | Required | Default                         |
| ----------------- | ----------------------------------- | -------- | ------------------------------- |
| `config-file`     | Path to repository config YAML file | No       | `.github/repository-config.yml` |
| `fail-on-missing` | Fail if config file is missing      | No       | `false`                         |

## Outputs

| Output       | Description                                                             |
| ------------ | ----------------------------------------------------------------------- |
| `config`     | Parsed configuration as JSON string                                     |
| `has-config` | Whether config file exists and was parsed successfully (`true`/`false`) |
| `raw-yaml`   | Raw YAML content (if exists)                                            |

## Example Repository Config

The action expects a YAML file like `.github/repository-config.yml`:

```yaml
# .github/repository-config.yml
ci:
  go:
    versions:
      - "1.23"
      - "1.24"
  python:
    versions:
      - "3.12"
      - "3.13"
  rust:
    versions:
      - "1.75"
  coverage:
    threshold: 85

release:
  go:
    enabled: true
  python:
    enabled: true
  docker:
    platforms:
      - "linux/amd64"
      - "linux/arm64"
```

## Step Summary Output

The action provides rich feedback in the GitHub Actions UI:

```
✅ Loaded config from `.github/repository-config.yml`

**Config sections:** `ci`, `release`, `docker`
```

## Error Handling

- **Missing config (default)**: Logs warning, continues with empty config `{}`
- **Missing config (fail-on-missing=true)**: Logs error, exits with code 1
- **Invalid YAML**: Logs error, continues with empty config or fails based on setting
- **File read error**: Logs error, exits with code 1

## Requirements

- Python 3.8+
- PyYAML (installed automatically if missing)

## License

MIT

## Author

jdfalk
