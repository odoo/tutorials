from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    property_ids = fields.One2many("estate.property", "property_type", string="Properties")

    _sql_constraints = [
    ('unique_property_type_name', 'UNIQUE(name)',
     'Property type name must be unique.'),
    ] 
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
      for rec in self:
        rec.offer_count = len(rec.offer_ids)
