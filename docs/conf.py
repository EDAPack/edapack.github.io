project = "EDAPack"
author = "EDAPack contributors"
copyright = "2024, EDAPack contributors"
release = "0.1"

extensions = ["myst_parser"]

# Copy the top-level package catalog verbatim into the site root so it is
# served at https://edapack.github.io/ivpm.yaml
html_extra_path = ["ivpm.yaml"]

html_theme = "alabaster"
html_title = "EDAPack"

html_theme_options = {
    "description": "Portable pre-built EDA tool binaries",
    "github_user": "EDAPack",
    "github_repo": "edapack.github.io",
    "github_button": True,
    "fixed_sidebar": True,
}
