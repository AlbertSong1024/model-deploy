"""Core model deployment functionality."""

import os
import subprocess
import sys
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

from rich.console import Console
from rich.panel import Panel

console = Console()


@dataclass
class DeployConfig:
    """Deployment configuration."""
    model_name: str
    framework: str = "vllm"
    port: int = 8000
    host: str = "0.0.0.0"
    gpu_layers: int = -1
    max_tokens: int = 2048
    temperature: float = 0.7
    extra_args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeployStatus:
    """Deployment status."""
    success: bool
    model: str
    framework: str
    url: str = ""
    pid: Optional[int] = None
    error: Optional[str] = None
    message: str = ""


def check_dependencies(framework: str) -> bool:
    """Check if required dependencies are installed."""
    deps = {"vllm": ["vllm"], "ollama": ["ollama"], "openai": ["openai"]}
    for pkg in deps.get(framework, []):
        result = subprocess.run([sys.executable, "-m", "pip", "show", pkg], capture_output=True)
        if result.returncode != 0:
            console.print(f"[red]Missing: {pkg}[/red]")
            console.print(f"[yellow]Install: pip install {pkg}[/yellow]")
            return False
    console.print("[green]All dependencies satisfied[/green]")
    return True


def deploy_vllm(config: DeployConfig) -> DeployStatus:
    """Deploy model using vLLM."""
    try:
        cmd = [
            "python", "-m", "vllm.entrypoints.openai.api_server",
            "--model", config.model_name,
            "--host", config.host,
            "--port", str(config.port),
            "--max-model-len", str(config.max_tokens),
        ]
        proc = subprocess.Popen(cmd)
        url = f"http://{config.host}:{config.port}/v1"
        return DeployStatus(success=True, model=config.model_name, framework="vllm", url=url, pid=proc.pid, message=f"vLLM server running at {url}")
    except Exception as e:
        return DeployStatus(success=False, model=config.model_name, framework="vllm", error=str(e))


def deploy_ollama(config: DeployConfig) -> DeployStatus:
    """Deploy model using Ollama."""
    try:
        subprocess.run(["ollama", "pull", config.model_name], check=True, capture_output=True)
        proc = subprocess.Popen(["ollama", "serve"])
        return DeployStatus(success=True, model=config.model_name, framework="ollama", url="http://localhost:11434/api", pid=proc.pid, message="Ollama server started")
    except subprocess.CalledProcessError as e:
        return DeployStatus(success=False, model=config.model_name, framework="ollama", error=str(e))
    except Exception as e:
        return DeployStatus(success=False, model=config.model_name, framework="ollama", error=str(e))


def deploy(config: DeployConfig) -> DeployStatus:
    """Deploy model using specified framework."""
    console.print(f"[bold blue]Deploying {config.model_name} ({config.framework})...[/bold blue]")
    if not check_dependencies(config.framework):
        return DeployStatus(success=False, model=config.model_name, framework=config.framework, error="Missing dependencies")
    frameworks = {"vllm": deploy_vllm, "ollama": deploy_ollama}
    deploy_fn = frameworks.get(config.framework)
    if not deploy_fn:
        return DeployStatus(success=False, model=config.model_name, framework=config.framework, error=f"Unknown framework: {config.framework}")
    return deploy_fn(config)


def stop_deployment(pid: int) -> bool:
    """Stop a deployment by PID."""
    try:
        subprocess.run(["kill", str(pid)], check=True)
        console.print(f"[green]Stopped process {pid}[/green]")
        return True
    except subprocess.CalledProcessError:
        console.print(f"[red]Failed to stop process {pid}[/red]")
        return False


def list_available_models(framework: str = "ollama") -> list:
    """List available models."""
    if framework == "ollama":
        try:
            import requests
            resp = requests.get("http://localhost:11434/api/tags", timeout=5)
            if resp.status_code == 200:
                return [m["name"] for m in resp.json().get("models", [])]
        except Exception:
            pass
    return []
