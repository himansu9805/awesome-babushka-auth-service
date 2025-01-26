"""Main module for the auth service."""

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"Hello": "World"}


def main():
    """Run the FastAPI application."""
    uvicorn.run(app)


if __name__ == "__main__":
    main()
