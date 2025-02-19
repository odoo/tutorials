"""
    estate_property.py

    Author: Hicham (hime)
"""

from odoo import models, fields
from .constants import (
    PROPERTY_ORM_NAME,
    PROPERTY_ORM_DESC,
    PROPERTY_DEFAULT_GARAGE,
    PROPERTY_DEFAULT_GARDEN,
    PROPERTY_DEFAULT_GARDEN_ORIENTATION_SELECTION,
    PROPERTY_GARDEN_ORIENTATION_SELECTION,
    PROPERTY_UI_GARDEN_ORIENTATION_SELECTION,
)

class Property(models.Model):
    _name = PROPERTY_ORM_NAME 
    _description = PROPERTY_ORM_DESC

    postcode = fields.Char(required=True)
    date_availability = fields.Date(required=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(required=True)
    bedrooms = fields.Integer(required=True) 
    living_area = fields.Integer(required=True)
    facades = fields.Integer(required=True)
    garage = fields.Boolean(required=False, default=PROPERTY_DEFAULT_GARAGE)
    garden = fields.Boolean(required=False, default=PROPERTY_DEFAULT_GARDEN)
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=PROPERTY_GARDEN_ORIENTATION_SELECTION,
        string=PROPERTY_UI_GARDEN_ORIENTATION_SELECTION,
        default=PROPERTY_DEFAULT_GARDEN_ORIENTATION_SELECTION,
    )
