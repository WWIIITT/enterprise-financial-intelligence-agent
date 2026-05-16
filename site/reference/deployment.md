# Deployment

## Knowledge Site

The knowledge site is designed for GitHub Pages.

1. Commit and push the `site/` directory and `.github/workflows/deploy-knowledge-site.yml`
2. In GitHub repository settings, enable Pages
3. Choose GitHub Actions as the build and deployment source
4. Push to `main` or run the workflow manually

Expected public URL:

```text
https://<github-user>.github.io/enterprise-financial-intelligence-agent/
```

## Dashboard And API

The current dashboard and backend remain local or deployable separately. The knowledge site is static and does not require the backend.

## Production Path

For production, deploy the backend, frontend dashboard, PostgreSQL, Qdrant, and Redis through a managed cloud or container platform. See `docs/deployment-roadmap.md` for the staged deployment plan.
