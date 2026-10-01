# Sandra Vargas Realtor Docs

This repository is a [Zensical](https://zensical.org) site. Configuration lives in `zensical.toml`.

## Local development

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the local docs server:

```bash
zensical serve
```

The site will be available at `http://127.0.0.1:8000`.

## Build

```bash
zensical build --strict
```

The generated site is written to `site/`.

## GitHub Pages deployment

The repository includes a GitHub Actions workflow at `.github/workflows/deploy-docs.yml`.

To publish successfully:

1. Push to the `main` branch.
2. In GitHub, open `Settings > Pages`.
3. Set the source to `GitHub Actions`.

After that, each push to `main` will build and deploy the documentation site automatically.
