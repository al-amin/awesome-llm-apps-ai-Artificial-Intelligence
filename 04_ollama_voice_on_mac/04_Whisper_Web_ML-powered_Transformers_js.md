https://github.com/xenova/whisper-web

# Whisper Web - Enhanced Setup Guide

[![ML-powered speech recognition](https://img.shields.io/badge/ML--powered-Speech%20Recognition-blue)](https://github.com/xenova/whisper-web)
[![Built with Transformers.js](https://img.shields.io/badge/Built%20with-🤗%20Transformers.js-yellow)](https://github.com/xenova/transformers.js)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> ML-powered speech recognition directly in your browser! Built with [🤗 Transformers.js](https://github.com/xenova/transformers.js).

## Overview

Whisper Web brings the power of OpenAI's Whisper speech recognition model directly to your web browser. This project enables real-time transcription of audio without sending any data to a server, preserving privacy and enabling offline usage.

Visit the [demo site](https://huggingface.co/spaces/Xenova/whisper-web) to try it out!

> [!IMPORTANT]  
> For GPU acceleration: Experimental WebGPU support is available in [this branch](https://github.com/xenova/whisper-web/tree/experimental-webgpu) ([demo](https://huggingface.co/spaces/Xenova/whisper-webgpu))

## Features

- ✅ **Privacy-focused**: All processing happens in your browser
- ✅ **No server required**: Works entirely client-side
- ✅ **Real-time transcription**: Transcribe as you speak
- ✅ **File upload support**: Process existing audio files
- ✅ **URL import**: Transcribe audio from web links
- ✅ **Mobile compatible**: Works on smartphones and tablets

## Getting Started

### Prerequisites

- Node.js (latest LTS version recommended)
- npm (comes with Node.js)
- Modern web browser (Chrome, Edge, Safari, or Firefox with Web Workers enabled)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/xenova/whisper-web.git
   cd whisper-web
   ```

2. **Run the professional development launcher**

   We've included an enhanced launcher script that handles dependency installation, environment verification, and server startup:

   ```bash
   ./run_dev.sh
   ```

   This script will:
   - Verify your Node.js and npm installation
   - Check and install dependencies if needed
   - Provide browser compatibility notes
   - Start the development server with visual feedback

   > If you encounter a permission error, make the script executable:
   > ```bash
   > chmod +x run_dev.sh
   > ```

3. **Open in your browser**

   Once the server is running, open [http://localhost:5173/](http://localhost:5173/) in your browser.

### Firefox Configuration

Firefox users need to enable Web Workers modules:

1. Open `about:config` in Firefox
2. Search for `dom.workers.modules.enabled`
3. Set it to `true`
4. Restart Firefox

See [GitHub issue #8](https://github.com/xenova/whisper-web/issues/8) for more details.

## Usage

### Live Recording

1. Click the microphone button to start recording
2. Speak clearly into your microphone
3. Click the stop button when finished
4. The transcription will appear in the text area

### Upload Audio File

1. Click the upload button
2. Select an audio file from your device
3. The transcription will begin automatically

### Transcribe from URL

1. Click the URL button
2. Enter the URL of an audio file
3. Click "Transcribe" to begin processing

## Development

### Project Structure

```
whisper-web/
├── public/          # Static assets
├── src/             # Source code
│   ├── components/  # React components
│   ├── hooks/       # Custom React hooks
│   ├── utils/       # Utility functions
│   └── worker.js    # Web Worker for ML processing
├── run_dev.sh       # Enhanced development launcher
└── package.json     # Project dependencies
```

### Available Scripts

- `./run_dev.sh` - Start the development server with enhanced feedback
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Check for code issues
- `npm run lint:fix` - Fix code issues automatically
- `npm run format` - Format code with Prettier

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - The original speech recognition model
- [Transformers.js](https://github.com/xenova/transformers.js) - ML models in JavaScript
- [Hugging Face](https://huggingface.co/) - For hosting the demo

---

*Built with ❤️ by the open-source community*
