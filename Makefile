# Create/update Python API documentation in Markdown format and output to README.md file.
# 
# -m			The modules.
# -I			A directory to use in the search for Python modules.
# --render-toc	Enable the rendering of the TOC in the "markdown" renderer.
# -v 			Increase log verbosity.
doc:
	pydoc-markdown -m sevp -m db -I . --render-toc -v > README.md

# Generate requirement file containing a pinned version of everything that is installed at the moment.
freeze:
	pip3 freeze > requirements.txt

# Instalar dependências (libs) com base no arquivo requirements.txt.
install-pkgs:
	pip3 install -r requirements.txt