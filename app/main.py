from __future__ import annotations

import uvicorn


def main() -> None:
    """Entry point to run the FastAPI application."""
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
