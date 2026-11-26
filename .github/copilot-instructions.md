# Copilot instructions

weatherdl downloads weather images (URLs built from `config.json`) and assembles them into a `briefing.pptx`. Python ≥3.14, managed with [uv](https://docs.astral.sh/uv/).

## Commands

```
uv sync --all-extras                              # set up env
uv run python src/main.py                         # run
uv run pytest                                     # all tests
uv run pytest tests/slides_parser_test.py::test_name   # single test
uv run pylint $(git ls-files '*.py')              # lint (CI)
uv run black . --check                            # format check (CI); drop --check to fix
uv lock                                           # after editing pyproject.toml deps
```

CI (`.github/workflows/ci.yml`) is the orchestrator: `check.yml` runs pytest, pylint and black (`uv sync --all-extras --frozen`), then build, release tests and release. On `v*` tags, `verify-version.yml` must pass first: the `pyproject.toml` `version` must match the tag (a leading `v` is ignored), so bump it before tagging. Binaries are built with PyInstaller (see `docs/CONTRIBUTING.md`; the pptx templates must be bundled via `--add-data`, and `config.json` is copied next to the executable).

## Architecture

Pipeline in `src/main.py`: `ApplicationConfig` → `Downloader(config).run()` → `Briefing(config).save_as("briefing.pptx")`.

- `ApplicationConfig` loads `config.json`, resolves `img_dir` (`~/` + `working_dir`, with strftime substitution of the start time) and calls `SlidesParser` to produce `config.slides`.
- `SlidesParser` expands each config item × `times` entry into a slide dict (`slide_number`, `title`, `file_name`, `url`, `hidden`). Time handling is the tricky part: `time` strings like `"1200"` or `"1200+1"` (HHMM plus optional day shift) are interpreted in the item's `time_zone` (default: display zone), converted to `url_time_zone` (default: the reference zone), then substituted into the URL via strftime. Metservice and MetVuw URLs are true UTC, so those items use `url_time_zone: "UTC"` with a UTC reference `time_zone`; slide titles are always shown in the display zone, so labels shift with DST while the URL hour stays fixed. There is no offset option: never shift URL times by fixed hours, since that breaks across DST. See `docs/configuration.md` for the config schema.
- `Downloader` and `Briefing` both consume `config.img_dir` and `config.slides`; images are matched to slides by the `file_name` basename (`NNN Title`) with an extension added from the detected image type, so the two must agree on naming.
- `utils.get_config_path()` finds `config.json` at the repo root when run as a script, or next to the executable when frozen by PyInstaller.

## Conventions

- Modules in `src/` import each other as top-level modules (`from utils import ...`); pytest sets `pythonpath = "src"` and `--import-mode=importlib`. Don't use package-relative imports.
- Tests live in `tests/*_test.py`; `tests/fixtures/config.json` is the config used by tests, and `freezegun` is used to fix time. The end-to-end test in `tests/main_test.py` performs real downloads.
- pylint is enforced; the codebase uses targeted `# pylint: disable=...` comments (e.g. `too-few-public-methods`, missing docstrings) rather than changing structure. Tests relax import-error and docstring rules via `pyproject.toml`.
- Dependencies are pinned exactly in `pyproject.toml` (prod in `dependencies`, dev/build in `[project.optional-dependencies]`); `uv.lock` must be regenerated after changes.
- Dependabot's uv updates fail if `tool.uv.required-version` is pinned older than Dependabot's supported uv; keep it a loose lower bound.
