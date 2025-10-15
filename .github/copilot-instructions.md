# Copilot Instructions for AI Agents

## 🎯 Project Overview

This project is a **local FastAPI server** designed to fetch song lyrics. It is intended to be used with Google Colab notebooks, specifically for projects like [colab-audio-dataset-forge](https://github.com/charge0315/colab-audio-dataset-forge). The server exposes an API that can be made accessible from the public internet using **ngrok**, allowing Colab environments to request lyrics from your local machine.

### Key Features

-   **Lyrics Fetching**: Retrieves song lyrics from the Genius API.
-   **Local Caching**: Caches fetched lyrics in a local `lyrics/` directory to minimize API calls and avoid rate limits.
-   **ngrok Integration**: Includes scripts to easily expose the local server to the internet, making it accessible from Google Colab.
-   **Simple API**: Provides a straightforward API for requesting lyrics by artist and title.

## 🛠️ Key Files

-   **`lyrics_api.py`**: The main FastAPI application file that defines the API endpoints.
-   **`fetch_lyrics.py`**: Contains the core logic for fetching lyrics from the Genius API and handling the local cache.
-   **`start_lyrics_server.bat` / `start_lyrics_server.sh`**: Convenience scripts for Windows and Linux/Mac to automatically set up the environment, start the FastAPI server, and launch ngrok.
-   **`start_ngrok.py`**: A Python script to start the ngrok tunnel.
-   **`requirements.txt`**: Lists the necessary Python dependencies.

## 💻 Developer Workflow

**1. Quick Start**

The easiest way to get the server running is to use the provided startup scripts.

-   **On Windows:**
    ```bash
    start_lyrics_server.bat
    ```
-   **On Linux/Mac:**
    ```bash
    chmod +x start_lyrics_server.sh
    ./start_lyrics_server.sh
    ```
These scripts will handle creating a virtual environment, installing dependencies, starting the FastAPI server, and creating an ngrok tunnel.

**2. Manual Setup and Execution**

If you prefer to run the components manually:

-   **Set up the environment:**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On Linux/Mac: source venv/bin/activate
    pip install -r requirements.txt
    ```

-   **Set your Genius API Key:**
    It is recommended to set your Genius API key as an environment variable.
    ```bash
    # On Windows:
    set GENIUS_API_KEY=your_genius_api_key_here
    # On Linux/Mac:
    export GENIUS_API_KEY=your_genius_api_key_here
    ```
    If not set, the script will fall back to a hardcoded key in `fetch_lyrics.py`.

-   **Start the FastAPI server:**
    In one terminal:
    ```bash
    uvicorn lyrics_api:app --reload --port 8000
    ```

-   **Start ngrok:**
    In a second terminal:
    ```bash
    python start_ngrok.py
    # or use the ngrok CLI:
    # ngrok http 8000
    ```

**3. Using the API from Google Colab**

Once the server is running and ngrok has provided a public URL (e.g., `https://xxxx.ngrok-free.app`), you need to configure your Colab notebook to use it.

In the Colab notebook (e.g., `audio_whisper_transcription.ipynb`):
```python
USE_LOCAL_LYRICS_API = True
LYRICS_API_URL = "https://your-ngrok-url.ngrok-free.app"
```
The notebook will then be able to send requests to your local server to fetch lyrics.

## 📝 Project-Specific Conventions

-   **Caching**: The server is designed to be cache-first. It always checks for a local copy of the lyrics in the `lyrics/` directory before making a request to the Genius API.
-   **API Key Management**: The preferred way to provide the Genius API key is through the `GENIUS_API_KEY` environment variable. A hardcoded fallback exists in `fetch_lyrics.py` but should be avoided in production or shared environments.
-   **ngrok Usage**: The project is built around the use of ngrok to bridge the gap between a local development server and a cloud-based environment like Google Colab. Be aware of the limitations of the free ngrok plan (e.g., session timeouts).
-   **API Endpoints**:
    -   `GET /healthz`: For health checks.
    -   `POST /api/v1/lyrics`: To request and cache lyrics.
    -   `GET /api/v1/lyrics`: To retrieve lyrics from the cache.
