"""Render the templates from instrument and piece objects."""
from jinja2 import Environment, PackageLoader
import os
from pathlib import Path

ENV = Environment(loader=PackageLoader('lyskel', 'templates'))


def render_instrument(instrument,
