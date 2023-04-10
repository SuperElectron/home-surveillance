from dotenv import load_dotenv

from app.core.config import load_settings
from app.api.api import initialize

def main() -> None:
    load_dotenv()
    load_settings()

    initialize()


if __name__ == "__main__":
    main()