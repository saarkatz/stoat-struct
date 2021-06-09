"""The registry module

This module supplies the bookkeeping functionality that enables the system keep
coherence between identical classes used in different places and to prevent the
generation of too many classes.
"""
from .registry import Registry
