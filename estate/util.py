def action(function):
    """When nothing is returned, return `True` as a default instead"""
    def action_wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        if result is None:
            return True
        return result
    return action_wrapper
