"""
constants.py

This module defines constants used across my real estate application.

As the project evolves, additional constants may be added here 
to maintain consistency and avoid hardcoded values in multiple places.

Author: Hicham (hime)

"""

# ORM Related fields

PROPERTY_ORM_NAME='estate'
PROPERTY_ORM_DESC='estate property'

# Default values

DEFAULT_PROPERTY_GARAGE=False
DEFAULT_PROPERTY_GARDEN=False
DEFAULT_PROPERTY_GARDEN_ORIENTATION_SELECTION='north'

PROPERTY_GARDEN_ORIENTATION_SELECTION=[
        ('north', 'North'), 
        ('south', 'South'), 
        ('east', 'East'), 
        ('west', 'West'),
]
