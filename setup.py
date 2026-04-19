# setup.py — compatibilidad con versiones antiguas de pip (<21.3)
# En versiones modernas de pip, pyproject.toml es suficiente.
# Este fichero existe por si el usuario tiene una versión antigua de pip
# y hace 'pip install -e .' sin soporte completo de pyproject.toml.
#
# No necesitas tocar nada aquí. Toda la configuración real está en pyproject.toml.

from setuptools import setup

setup()
