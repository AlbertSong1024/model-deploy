# Model Deploy

> 一键模型部署工具，支持 vLLM、Ollama 和 OpenAI 兼容 API

## 特性

- **多框架支持**: vLLM, Ollama, OpenAI 兼容端点
- **一条命令部署**: `model-deploy serve llama3`
- **OpenAI 兼容 API**: 可直接替换 OpenAI 端点
- **GPU 优化**: 自动 GPU 层分配

## 快速开始

```bash
pip install model-deploy

# 使用 vLLM 部署
model-deploy serve meta-llama/Llama-3.1-8B --framework vllm --port 8000

# 使用 Ollama 部署
model-deploy serve llama3 --framework ollama
```

## 许可证

MIT
