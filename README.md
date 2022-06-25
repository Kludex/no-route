<h1 align="center">
    <strong>no-route</strong>
</h1>
<p align="center">
    <a href="https://pypi.org/project/no-route" target="_blank">
        <img src="https://img.shields.io/pypi/v/no-route" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/no-route">
    <img src="https://img.shields.io/github/license/Kludex/no-route">
</p>

Yet another opinionated formatter. Turns `@app.route(..., methods=[<method>])` into `@app.<method>(...)`.

Works with `Flask` and `FastAPI`.

Example:

```python
@app.route("/", methods=["GET"])
def home():
  ...
```

Into:

```python
@app.get("/")
def home():
  ...
```

## Installation

```bash
pip install no-route
```

## License

This project is licensed under the terms of the MIT license.
