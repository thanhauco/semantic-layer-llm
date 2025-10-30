import click
from semantic_layer.sdk.client import SemanticLayerClient

@click.group()
def cli():
    """Semantic Layer CLI"""
    pass

@cli.command()
@click.option('--metrics', '-m', multiple=True, required=True)
@click.option('--dimensions', '-d', multiple=True)
def query(metrics, dimensions):
    """Execute a query"""
    client = SemanticLayerClient("http://localhost:8000")
    result = client.query(list(metrics), list(dimensions))
    click.echo(result)

@cli.command()
def list_metrics():
    """List all metrics"""
    client = SemanticLayerClient("http://localhost:8000")
    metrics = client.list_metrics()
    for metric in metrics:
        click.echo(f"- {metric['name']}: {metric.get('description', 'No description')}")

if __name__ == '__main__':
    cli()
