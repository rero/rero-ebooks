---
title: Release notes
copyright: Copyright (C) 2020 RERO
license: GNU Affero General Public License
---

# Release notes

## v0.5.0

## Harvesting

- Adds XSL style to OAI2D.
- Deletes resource links to unavailable ebooks during harvesting.
- Fixes connection issues with `ApiHarvestConfig`.
- Deactivates OAI harvesting tasks, that should be a crontab job.
- Fixes API blueprint configuration.

### Instance

- Updates `invenio` to version `3.2`, and then `3.3`.
- Updates ElasticSearch to version `7`.
- Updates PostgreSQL to version `12`.
- Updates `nginx` configuration to disable restriction on request level.
- Updates `bootstrap` script to [rero-ils][1] practices.
- Updates `Pipfile` and `Pipfile.lock` files to [rero-ils][1] practices. Then,
  moves to `poetry`.
- Deletes `invenio-records` `CLI` (deprecated).
- Moves to GitHub actions for *Continuous integration* (CI).
- Moves assets management to webpack.

### Issues

- [#28][i28]: Broken links on homepage.

[1]: https://github.com/rero/rero-ils
[i28]: https://github.com/rero/rero-ebooks/issues/28
