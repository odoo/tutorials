from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Types"
    _order = "sequence"
    
    _sql_constraints = [
        ("unique_property_type_name", "UNIQUE(name)", "Type Name must be Unique")
    ]

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer('Sequence', default=1, help="order property-lower is better")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Number of Offers", compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property in self:
            property.offer_count = len(property.offer_ids)
