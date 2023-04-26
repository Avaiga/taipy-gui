import warnings

class TaipyGuiWarning(UserWarning):
    pass

def warnings_warn(message: str):
    warnings.warn(message, TaipyGuiWarning)
