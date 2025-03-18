# A-eye: AI-Powered Vision Assistant for the Visually Impaired

## AI-On-the-Edge Hackathon Project

This project was developed for the "AI - On the edge" Hackathon, which focused on creating innovative AI solutions that can run efficiently on edge devices. The hackathon challenged participants to develop applications that leverage AI capabilities while minimizing reliance on cloud infrastructure, enabling functionality in environments with limited connectivity.

## Project Overview

A-eye is an AI-powered vision assistant designed to help visually impaired individuals navigate their surroundings. It's designed to fit on an edge device such as a raspberry pi (8Go RAM minimum). 

The system:
1. Captures images from the user's environment
2. Receives voice commands/questions from the user
3. Processes the visual information using advanced AI models
4. Provides spoken descriptions and guidance based on what it "sees"

The system is designed to be conversational, maintaining context from previous interactions to provide more useful assistance over time.

## How It Works

A-eye consists of the following components:

1. **Image Processing**: The system processes images captured from the user's point of view
2. **Speech-to-Text**: User voice commands are converted to text using Whisper AI
3. **AI Vision Analysis**: The Pixtral-12b model analyzes images and generates appropriate responses
4. **Text-to-Speech**: Responses are converted to spoken audio using pyttsx3
5. **Conversation History**: The system maintains context for more natural interactions

## Technical Architecture

- **Backend Server**: Flask-based API that processes images and audio
- **AI Models**:
  - Whisper (OpenAI) for speech recognition (on edge)
  - Pixtral-12b-2409 for image analysis and contextual understanding - designed to be replaced by a smaller model directly on edge
- **Data Flow**:
  - Client captures and sends images and audio to the server
  - Server processes inputs and generates appropriate responses
  - Responses are sent back to the client as text and speech

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- API key for OpenAI services

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/colinfrisch/A-eye.git
   cd A-eye/final
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create an `API_setup.py` file with your OpenAI API key:
   ```python
   from openai import OpenAI
   
   # Initialize the OpenAI client
   client = OpenAI(api_key="your-openai-api-key-here")
   ```

### Running the Application

1. Start the server:
   ```
   python process_image.py
   ```

2. In a separate terminal, run the client example (modify paths as needed):
   ```
   python client_example.py
   ```

## Usage Examples

The system is designed to respond to voice commands such as:

- "What objects are in front of me?"
- "Is there a path clear to walk?"
- "Can you read the sign ahead?"

The AI will analyze the images and provide concise, helpful responses focused on helping the visually impaired user navigate their environment.

## Project Structure

- `process_image.py`: Main server application with Flask API endpoints
- `client_example.py`: Example client demonstrating how to interact with the API
- `chat_history.json`: Stores conversation history for contextual awareness
- `requirements.txt`: List of required Python packages

## Future Improvements

- Improve edge processing capabilities for lower latency (replace pixtral 12B)
- Implement haptic feedback integration
- Create mobile applications for easier deployment
- Support for multiple languages

## Contributors

- Léo Lebuhotel
- Othmane Menkor
- Yiwen Mai
- Dorian Boucher
- Colin Frisch
