"""
    estate_property.py

    Author: Hicham (hime)
"""

from odoo import models, fields
from .constants import (
    PROPERTY_ORM_NAME,
    PROPERTY_ORM_DESC,
    DEFAULT_PROPERTY_GARAGE,
    DEFAULT_PROPERTY_GARDEN,
    DEFAULT_PROPERTY_GARDEN_ORIENTATION_SELECTION,
    PROPERTY_GARDEN_ORIENTATION_SELECTION,
)

class Property(models.Model):
    _name = "estate" 
    _description = "estate property"

    postcode = fields.Char(required=True)
    date_availability = fields.Date(required=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(reqiured=True)
    bedrooms = fields.Integer(required=True) 
    living_area = fields.Integer(required=True)
    facades = fields.Integer(required=True)
    garage = fields.Boolean(required=False, default=DEFAULT_PROPERTY_GARAGE)
    garden = fields.Boolean(required=False, default=DEFAULT_PROPERTY_GARDEN)
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=PROPERTY_GARDEN_ORIENTATION_SELECTION,
        string="Garden Orientation",
        default=DEFAULT_PROPERTY_GARDEN_ORIENTATION_SELECTION,
    )
