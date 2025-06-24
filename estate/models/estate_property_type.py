from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Store Real Estate Properties Types"
    _order = "sequence, name"

    name = fields.Char("Estate Type Name", required=True, translate=True)
    sequence = fields.Integer(default=1, help="Used to order property types. Lower is better.")
    offer_count = fields.Integer(compute='_compute_offer_count')
    
    # Relations
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string="Offers"
    )
    
    # Computed Functions
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for estate_type in self:
            estate_type.offer_count = len(estate_type.offer_ids)
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]