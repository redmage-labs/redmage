import logging

# setup logging before importing app
logging.basicConfig()
logging.getLogger("redmage").setLevel(logging.DEBUG)

import uvicorn

from examples.todo_jinja2 import app

if __name__ == "__main__":
    uvicorn.run(app.starlette, port=8000)
