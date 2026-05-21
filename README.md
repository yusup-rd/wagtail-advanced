# Wagtail Advanced — Project Summary

## Project Overview
- A Wagtail-based blog project built during an Advanced Wagtail course. It demonstrates custom page models, StreamField usage with custom blocks, internationalization, and Wagtail's API and admin features.

## Key Features
- **Custom Page Models:** `HomePage`, `BlogIndex`, `BlogDetail` implemented under the `blogpages` app. See [blogpages/models.py](blogpages/models.py).
- **StreamField & Custom Blocks:** Custom blocks such as text, image, FAQ list and carousel are defined in [blocks/blocks.py](blocks/blocks.py) and used in `BlogDetail`.
- **Custom Image/Document Models:** `CustomImage` and `CustomDocument` extend Wagtail models. See [images/models.py](images/models.py) and [documents/models.py](documents/models.py).
- **Internationalization:** `wagtail-localize` is enabled and languages are configured in [blog/settings/base.py](blog/settings/base.py).
- **Wagtail API:** A Wagtail API router is configured in [blog/api.py](blog/api.py) and mounted at `/api/v2/` in [blog/urls.py](blog/urls.py).
- **Search & Sitemap:** Site search and sitemap integration via Wagtail and Django are present (see [search/views.py](search/views.py) and [blog/urls.py](blog/urls.py)).
- **Tailwind CSS:** Frontend styles are managed with Tailwind. See `package.json` (scripts) and `tailwind.config.js`.
- **Validation & Admin UX:** Custom `clean()` methods and helpful admin panels improve content quality and editor experience.

## Notable Files
- [requirements.txt](requirements.txt)
- [manage.py](manage.py)
- [blog/settings/base.py](blog/settings/base.py)
- [blog/settings/dev.py](blog/settings/dev.py)
- [blogpages/models.py](blogpages/models.py)
- [blocks/blocks.py](blocks/blocks.py)
- [images/models.py](images/models.py)
- [documents/models.py](documents/models.py)
- [blog/api.py](blog/api.py)
- [blog/urls.py](blog/urls.py)

## How to run (development)
1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell (Windows)
```

2. Install Python requirements:

```bash
pip install -r requirements.txt
```

3. Install frontend dependencies and build CSS (Node.js required):

```bash
npm install
npm run build:css   # or `npm run watch:css` during development
```

4. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

Visit http://localhost:8000/ for the site and http://localhost:8000/admin/ for the Wagtail admin.

## What I learned (summary)
- How Wagtail page models inherit from `Page` and how to restrict parent/subpage types.
- Building flexible content with `StreamField` and creating custom block types for rich, reusable content structures.
- Extending Wagtail's image and document models to add custom metadata (captions, descriptions).
- Using `wagtail-localize` and Django's i18n to support multiple languages and localized content.
- Exposing content via Wagtail's API and customizing serialization for related data (example: `AuthorSerializer`).
- Improving editor UX with admin panels, inline galleries, validation (`clean()`), and permission-aware panels.
- Integrating Tailwind CSS into a Django/Wagtail workflow for modern styling.

## Next steps / Suggestions
- Add tests that exercise page rendering and block validation.
- Add CI configuration to run `flake8`/`pytest` and build CSS.
- Consider deploying with a production-ready static/media setup (S3, WhiteNoise) and configuring secret management.

---
If you want, I can:
- add this README to the repo (already staged here), or
- expand any section with more details or examples (e.g., describe the StreamField block implementations or add screenshots).
