
__version__ = "0.1.2"

def get_version_on_platform() -> str:
    """
    Returns the version of the library along with the platform information.
    :return: A string containing the version and platform information.
    """
    import platform
    return f"v{__version__} on {platform.python_version()}"