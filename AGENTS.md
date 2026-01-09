# Agent Preferences (Project Notes)

## Testing style
- Use `pytest` for unit tests.
- Use `assertpy` for fluent assertions (C#-style), e.g. `assert_that(actual).is_equal_to(expected)`.
- Structure each test with explicit comments: `# Arrange`, `# Act`, `# Assert` (or `# Act / Assert` when combined).

## Project goals
- This is a pet project for learning data structures and algorithms (DSA).
- Prefer answers that teach: explain the “why”, suggest small exercises, and point out common pitfalls when relevant.

## Python style (3.13/3.14)
- Target modern Python (`>=3.13`, ideally `3.14`) and prefer idiomatic Python.
- Follow common conventions and standards (PEP 8, clear naming, small functions, good error messages).
- Prefer type hints and modern typing syntax where appropriate.
- Prefer standard library best practices (e.g., `pathlib`, context managers, `dataclasses` when useful, f-strings).
- Method order in classes: `__init__`, dunder methods (e.g., `__iter__`), then public API grouped by purpose, then
  private helpers.

## TDD constraint
- When doing test-first/TDD work, do **not** implement production code for the feature under test unless explicitly requested; tests should define the expected contract and let the implementation be developed separately.

## Running tests
- Run the suite with `python -m pytest -q`.
