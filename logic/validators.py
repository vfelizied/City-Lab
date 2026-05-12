def validate_report(name, location, description):
    """Validate inputs."""
    if not location:
        return "Falta ubicación"
    if not description:
        return "Falta descripción"
    return None
