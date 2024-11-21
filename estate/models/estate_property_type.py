# licence

from odoo import fields
from odoo import models
from odoo import api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property type"
    _order = "name asc"

    name = fields.Char("Type", required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types manually.")
    description = fields.Text("Type description")
    # Relational
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer("Offer count", compute='_compute_offer_count')
    # Constraints
    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The property type name must be unique'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
