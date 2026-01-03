# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-20

### Added

- Initial release of load-config-action
- Support for loading and parsing `.github/repository-config.yml`
- Automatic PyYAML installation
- Graceful fallback handling when config is missing
- Optional `fail-on-missing` input for strict validation
- Rich step summaries with config sections
- JSON output for downstream GitHub Actions

## [Unreleased]

### Added

- Dockerized execution path controlled by `use-docker`/`docker-image`
- Automated GHCR publish workflow with digest pinning and tag bump

### Changed

- Updated composite action outputs to support host and docker paths

### Security

- Container base pinned by digest for reproducible builds
