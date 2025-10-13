# Conversational Emotional Support Agent

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![Framework](https://img.shields.io/badge/Framework-LangChain-blueviolet.svg)

A real-time, voice-based AI companion built with LangChain, designed to listen, understand the user's emotional state, and respond with context-aware empathy.

---

## 📜 Table of Contents

- [About The Project](#about-the-project)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 About The Project

The **Conversational Emotional Support Agent** is a sophisticated Python application that provides a hands-free, supportive conversational space. Moving beyond simple task-oriented commands, this agent focuses on the nuances of human emotion. It actively listens to the user, analyzes their words, and crafts a unique, empathetic response in real-time.

Built with **LangChain**, the project leverages modern AI capabilities to manage conversation history, stream responses, and even perform parallel analyses on the user's input—all to create a more natural and supportive interaction.

The primary goal is to simulate a patient, non-judgmental, and caring conversation, offering users a safe environment to express their feelings and receive a thoughtful summary of their emotional journey afterward.



---

## ✨ Key Features

-   **Real-time Voice Interaction**: Fully hands-free conversation using a local microphone and speakers.
-   **LangChain Integration**: The core logic is structured with LangChain Expression Language (LCEL) for modular, powerful, and streamable AI chains.
-   **Parallel Processing**: Simultaneously generates an empathetic response, extracts key topics, and classifies user intent from a single utterance.
-   **"Barge-In" Functionality**: Users can interrupt the AI at any time by speaking, creating a natural, fluid conversational turn-taking.
-   **Dynamic Voice Activity Detection (VAD)**: Automatically detects when the user starts and stops speaking, eliminating the need for fixed recording times.
-   **Post-Conversation Summary**: Generates a concise summary of the user's emotional arc throughout the dialogue.

---

## ⚙️ System Architecture

The agent processes information in a continuous, optimized loop. The core logic is orchestrated by `main.py`, which manages the audio I/O and the conversational state.

**Data Flow:**
`Microphone (VAD)` → `Audio File` → `Speech-to-Text (Whisper)` → `User Text` → `LangChain Parallel Chains (LLM)` → `Empathetic Response & Analysis` → `Text-to-Speech (TTS)` → `Audio Playback (Interruptible)`

---

## 🛠️ Technology Stack

-   **Language**: Python 3.10
-   **Core Framework**: **LangChain**
-   **AI Services**:
    -   **OpenAI API**:
        -   `whisper-1` for Speech-to-Text
        -   `gpt-4o` for Language Model tasks
        -   `tts-1` for Text-to-Speech
-   **Audio Handling**:
    -   **Sounddevice**: For real-time audio recording and playback.
    -   **pydub**: To handle MP3 audio data for interruptible playback.
    -   **NumPy / SciPy**: For numerical audio data processing.
-   **Environment Management**:
    -   **python-dotenv**: For securely managing API keys.

---

## 🚀 Getting Started

Follow these steps to get the agent running on your local machine.

### Prerequisites

-   **Python 3.10**.
-   An **OpenAI API Key**.
-   **FFmpeg**: A required dependency for `pydub`.
    -   **macOS (via Homebrew)**: `brew install ffmpeg`
    -   **Debian/Ubuntu**: `sudo apt-get install ffmpeg`
    -   **Windows**: Download binaries from the [official FFmpeg site](https://ffmpeg.org/download.html) and add the `bin` folder to your system's PATH.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/mehedihasanmir/Conversational-Emotional-Support-Agent.git](https://github.com/mehedihasanmir/Conversational-Emotional-Support-Agent.git)
    cd Conversational-Emotional-Support-Agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv myenv
    source myenv/bin/activate

    # For Windows
    python -m venv myenv
    .\myenv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your_secret_openai_api_key_here"
    ```

---

## ▶️ Usage

Once the setup is complete, run the application from your terminal:

```bash
python main.py
```

The agent will greet you. Begin speaking when you see the `🤫 Listening...` prompt. To end the conversation, simply say "**goodbye**."

---

## 🎛️ Configuration

For the best experience, you may need to tune the Voice Activity Detection (VAD) parameters in `audio_handler.py` based on your microphone and environment.

-   **`SILENCE_THRESHOLD`**: The volume level required to trigger a recording. Increase if background noise causes false triggers; decrease if your quiet voice isn't being detected.
-   **`SILENCE_DURATION`**: The length of silence (in seconds) that ends the recording. Increase if you're being cut off mid-sentence; decrease if there's a long pause after you finish speaking.

---

## 🗺️ Roadmap

-   [ ] **Integrate True Streaming STT/TTS**: Replace batch APIs with streaming services (e.g., Deepgram, ElevenLabs) for radically lower latency.
-   [ ] **Implement Wake Word Detection**: Add a wake word (e.g., "Hey, Assistant") so the agent isn't always listening.
-   [ ] **Add Long-Term Memory**: Use a vector database to give the agent memory of past conversations for more personalized interactions.

See the [open issues](https://github.com/mehedihasanmir/Conversational-Emotional-Support-Agent/issues) for a full list of proposed features (and known issues).

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## ⚖️ License

Distributed under the MIT License.