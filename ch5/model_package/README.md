__version_info__ = (0, 1, 0)
__version__ = ".".join([str(n) for n in __version_info__])

# a display name for the model
__display_name__ = "Churn Model"

# returning the package name as the qualified name for the model
__qualified_name__ = __name__.split(".")[0]

# a description of the model
__description__ = "A machine learning model for predicting the species of a flower based on its measurements."