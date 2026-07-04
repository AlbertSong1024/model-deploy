"""CLI for model-deploy."""

import click
from rich.console import Console
from rich.panel import Panel

from . import __version__
from .core import DeployConfig, deploy, list_available_models, stop_deployment

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="model-deploy")
def cli():
    """One-click model deployment with vLLM, Ollama, and OpenAI compatible APIs."""
    pass


@cli.command()
@click.argument("model")
@click.option("--framework", "-f", type=click.Choice(["vllm", "ollama", "openai"]), default="vllm")
@click.option("--port", "-p", default=8000, help="Port to serve on")
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to")
@click.option("--max-tokens", "-m", default=2048, help="Max tokens")
@click.option("--gpu-layers", "-g", default=-1, help="GPU layers")
def serve(model, framework, port, host, max_tokens, gpu_layers):
    """Deploy a model."""
    config = DeployConfig(model_name=model, framework=framework, port=port, host=host, max_tokens=max_tokens, gpu_layers=gpu_layers)
    status = deploy(config)
    if status.success:
        console.print(Panel(status.message, border_style="green"))
        console.print(f"[bold]Model:[/bold] {status.model}")
        console.print(f"[bold]Framework:[/bold] {status.framework}")
        console.print(f"[bold]URL:[/bold] {status.url}")
    else:
        console.print(Panel(f"Failed: {status.error}", border_style="red"))


@cli.command()
@click.argument("pid", type=int)
def stop(pid):
    """Stop a deployment."""
    stop_deployment(pid)


@cli.command()
@click.option("--framework", "-f", default="ollama")
def list_models(framework):
    """List available models."""
    models = list_available_models(framework)
    if models:
        console.print(f"[bold green]{len(models)} models available:[/bold green]")
        for m in models:
            console.print(f"  - {m}")
    else:
        console.print("[yellow]No models found[/yellow]")


if __name__ == "__main__":
    cli()
