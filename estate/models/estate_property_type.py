from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type model"
    _order = "sequence,name"

    name = fields.Char(required = True)
    property_ids = fields.One2many(comodel_name="estate_property", inverse_name = "property_type_id")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many(comodel_name="estate_property_offer", inverse_name = "property_type_id")
    offer_count = fields.Integer(compute = "_compute_offer_count")



    _sql_constraints = [
        ('is_property_type_unique', 'UNIQUE(name)', 'Property type name must be unique!')
    ]


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
        