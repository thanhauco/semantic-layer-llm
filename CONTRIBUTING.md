# Contributing

## Development Setup

```bash
git clone https://github.com/yourorg/semantic-layer.git
cd semantic-layer
poetry install
poetry run pytest
```

## Code Style

We use Black for formatting:
```bash
poetry run black .
```

## Testing

```bash
poetry run pytest
poetry run pytest --cov
```

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a PR
