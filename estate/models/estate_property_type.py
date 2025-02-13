from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"
    _order = 'sequence'
    _sql_constraints = [
        ('check_name', 'unique(name)', ('Property Type must be UNIQUE.'))
    ]

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property. Lower is better.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties") 
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')
    
    # compute offer count of that property type
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property in self:
            property.offer_count = len(property.offer_ids)
