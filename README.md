# Pydantic AI with Mem0

This project demonstrates the integration of Pydantic AI with Mem0 for building a conversational AI assistant with memory capabilities. The assistant can retrieve relevant memories from previous conversations and provides responses in Portuguese (pt-BR).

## Features

- Conversational AI using Pydantic AI and OpenAI models
- Memory storage and retrieval using Mem0
- Custom asynchronous wrapper for Mem0 operations (AsyncMemory)
- Context-aware responses based on user's past interactions
- Tool integration for retrieving current date and relevant memories

## Requirements

- Python 3.10+
- Postgres with pgvector extension for vector storage

## Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/pydantic-ai-mem0.git
cd pydantic-ai-mem0
```

2. Set up the environment

```bash
# Create a virtual environment using uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies using uv
uv pip install -r pyproject.toml
```

3. Configure environment variables

Create a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY="your-openai-api-key"
PGVECTOR_HOST="your-postgres-host"
PGVECTOR_PORT="your-postgres-port"
PGVECTOR_USER="your-postgres-user"
PGVECTOR_PASSWORD="your-postgres-password"
```

4. Run the application

```bash
python main.py
```

## Usage

After starting the application, you can interact with the assistant through the command line. Type your message and press Enter to receive a response. The assistant will remember previous interactions and use them to provide context-aware responses.

To exit the conversation, type `quit`.

## Project Structure

- `main.py`: Main application file with agent configuration and runtime loop
- `mem0_settings.py`: Configuration for Mem0 memory system
- `async_mem0.py`: Asynchronous wrapper for Mem0 memory operations
- `pyproject.toml`: Project dependencies

## License

See the [LICENSE](LICENSE) file for details.
