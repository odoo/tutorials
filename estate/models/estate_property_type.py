from odoo import api, fields, models
 
class EstatePropertyType(models.Model):
    '''Estate property type'''
    _name = "estate.property.type"
    _description = "Type of a property"
    _order = "name"

    name = fields.Char(required=True, string="Type")
    property_ids = fields.One2many("estate.property", "property_type_id", string = "Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string = "Offers")
    offer_count = fields.Integer("Offer count", compute = "_compute_offer_count")

    _sql_constraints = [('unique_type', 'unique(name)', 'The type already exist !')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
