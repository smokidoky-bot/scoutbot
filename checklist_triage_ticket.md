
# Improvements for the Triage prototype script:

- API key is in the code
- code is not on GitHub
- filename not ideal
- should import data from JSON file
- API key should be in .env file, use it in Python file
- no .gitignore
- split prompt in system + user prompt
- explicitly add expected output format (e.g. JSON)
- feature missing: team assignment
- package environment: py version + lib version, pyproject.toml
- examples for JSON output in prompt
- validate the result with LLM or other
- make categories a Literal
- use structured output of the model
- regex for validation
- user can do prompt injection
- user could submit very long text, set maximum length
- make options (model + max tokens) configurable (pydantic, configparser)
- uses haiku by default (cheap, good)
- create a uv environment
- no error handling (try.. except)
- monitor token usage/limits
- write unit test for the script
- the unit test must not consume tokens -> there should be a way to test without connecting to the API (mock, stub, monkeypatch, config setting)
- use a generic library to make it easy to switch to a different LLM (e.g. https://developers.openai.com/api/docs/libraries)
- uv python pin 3.13.17
- uv init --bare