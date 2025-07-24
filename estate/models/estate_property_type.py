# Odoo Imports
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    # -----------------------------
    # Fields
    # -----------------------------
    name = fields.Char(string='Property Type', required=True, help='Name of the property type (e.g., Apartment, House).')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties', help='Properties categorized under this type.')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers', help='Offers associated with properties of this type.')
    sequence = fields.Integer(string='Sequence', default=10, help='Used to order property types in lists and views.')
    offer_count = fields.Integer(string='Number of Offers', compute='_compute_offer_count', help='Total number of offers made on properties of this type.')

    # -----------------------------
    # SQL Constraints
    # -----------------------------
    _sql_constraints = [
        ('uniq_property_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
    ]

    # -----------------------------
    # Compute Function
    # -----------------------------
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        """
        Compute the total number of offers associated with this property type.
        """
        for record in self:
            record.offer_count = len(record.offer_ids) if hasattr(
                record, 'offer_ids') else 0
