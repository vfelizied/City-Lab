def validate_report(name, location, description):
    if not location or len(location.strip()) < 3:
        return "La ubicación es demasiado corta"

    if not description or len(description.strip()) < 10:
        return "Describe el problema con más detalle (mínimo 10 caracteres)"

    return None
