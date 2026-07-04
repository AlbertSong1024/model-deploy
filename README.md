# Model Deploy

> One-click model deployment with vLLM, Ollama, and OpenAI compatible APIs

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- **Multi-Framework**: vLLM, Ollama, OpenAI compatible endpoints
- **One-Command Deploy**: `model-deploy serve llama3`
- **OpenAI Compatible API**: Drop-in replacement for OpenAI endpoints
- **GPU Optimization**: Automatic GPU layer allocation

## Quick Start

```bash
pip install model-deploy

# Deploy with vLLM
model-deploy serve meta-llama/Llama-3.1-8B --framework vllm --port 8000

# Deploy with Ollama
model-deploy serve llama3 --framework ollama

# List available models
model-deploy list-models
```

## API Usage

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
response = client.chat.completions.create(model="llama3", messages=[{"role": "user", "content": "Hello!"}])
```

## License

MIT
