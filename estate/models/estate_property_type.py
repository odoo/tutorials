   # Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    
    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count', store=True)  
    _sql_constraints = [
        ('check_type_name', "UNIQUE(name)", "Type name must be unique. Please choose a different name.")
    ]
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property in self:
            property.offer_count = len(property.offer_ids)
