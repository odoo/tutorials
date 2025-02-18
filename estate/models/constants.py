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

PROPERTY_DEFAULT_GARAGE=False
PROPERTY_DEFAULT_GARDEN=False
PROPERTY_DEFAULT_GARDEN_ORIENTATION_SELECTION='north'

PROPERTY_UI_GARDEN_ORIENTATION_SELECTION='Garden Orientation'
PROPERTY_GARDEN_ORIENTATION_SELECTION=[
        ('north', 'North'), 
        ('south', 'South'), 
        ('east', 'East'), 
        ('west', 'West'),
]
