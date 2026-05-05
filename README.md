## Prerequisites

You will need [`uv`](https://docs.astral.sh/uv/) installed to be able to install dependencies and run the project.
Additionally you can use [`just`](https://just.systems/man/en/) to run commands more easily.

Next you need to setup the database by running `just setup_db` or `uv run python create_db.py`.

Then you can run the app by running `just dev`, `uv run flask --app main run` (you can add `--debug` at the end)
or `uv run python main.py` should also work.

## Commands

- `just install` - install dependencies
- `just setup_db` - setup the database
- `just dev` - run the dev server
- `just lint` - fix syntax issues
- `just format` - format the code

## Testing with `curl`

```sh
curl http:/localhost:5000
```

- `-X` - HTTP method (default is `GET`)
- `-H` - add a header
- `-d` - the request body data
- `-i` - include response headers in output
- `-v` - verbose
- `-o` - output to a file

### `GET`

```sh
curl -i http://localhost:5000/api/users
```

```sh
curl -i http://localhost:5000/api/users/{public_id}
```

### `POST`

```sh
curl -i -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com", "password": "12345"}'
```

### `PUT/PATCH`

```sh
curl -i -X PATCH http://localhost:5000/api/users/{public_id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@email.com", "password": "123456"}'
```

### `DELETE`

```sh
curl -i -X DELETE http://localhost:5000/api/users/{public_id}
```

## Links

- [Flask Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
- [HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)
