# greet.py — a tiny module with one public function.
# Anything not starting with an underscore is considered public.

def greet(name):
    """Return a friendly greeting."""
    return f"Hello, {name}! Welcome to modules."

def _secret():
    """Leading underscore signals 'internal use only'."""
    return "ssssh"