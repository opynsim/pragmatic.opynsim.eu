import zipfile
from pathlib import Path
from sphinx.util import logging

project = 'Pragmatic Musculoskeletal Modelling'
copyright = '2026, Contributors to the Pragmatic Musculoskeletal Modelling Repository'
author = 'The Musculoskeletal Modelling Community'
github_username = 'opynsim'
github_repository = 'https://github.com/opynsim/pragmatic.opynsim.eu'

# Number figures (e.g. Fig. 1, Fig. 2)
numfig = True

extensions = [
    "sphinx_copybutton",
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_logo = '_static/banner_vertical.svg'
html_favicon = '_static/logo.svg'
html_theme_options = {
    # Remove search/persistent components from the header
    "navbar_persistent": [],
    "navbar_start": [],
    "navbar_center": [],
    "navbar_end": [],

    # Disable specific top-right action buttons
    "use_download_button": False,
    "use_fullscreen_button": False,
    "use_repository_button": False,
}

logger = logging.getLogger(__name__)
def generate_pragmatic_resources_zip(app):
    zip_filename = "pragmatic_resources.zip"

    # Skip non-HTML builders (e.g., pdf, text)
    if app.builder.name not in ("html", "dirhtml"):
        logger.info(f"Skipping {zip_filename} generation: only applicable to html builders")
        return

    src_dir = Path(app.srcdir) / "../pragmatic_resources"
    out_dir = Path(app.outdir)
    zip_path = out_dir / zip_filename

    assert src_dir.exists(), f"{src_dir} does not exist"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Only rebuild if the zip is older than any resource in
    # `pragmatic_resources/`.
    zip_mtime = zip_path.stat().st_mtime if zip_path.exists() else 0
    needs_rebuild = not zip_path.exists()
    if not needs_rebuild:
        for file in src_dir.rglob("*"):
            if file.is_file() and file.stat().st_mtime > zip_mtime:
                needs_rebuild = True
                break

    if needs_rebuild:
        logger.info(f"packaging resources: {src_dir.name} -> {zip_path.name}...")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in src_dir.rglob("*"):
                if file.is_file():
                    arcname = src_dir.name / file.relative_to(src_dir)
                    zf.write(file, arcname=arcname)
                    logger.debug(f"Added {arcname} to {zip_path.name}")

def setup(app):
    app.connect("builder-inited", generate_pragmatic_resources_zip)
