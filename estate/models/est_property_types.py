from odoo import models, fields, api

class EstateType(models.Model):
    _name = "est.property.type"
    _description = "Property types"
    _order = "sequence,name"

    _check_name = models.Constraint(
        'unique(name)',
        'There is already a property type with that name!',
    )

    name = fields.Char("name", required=True)
    sequence = fields.Integer(default=1)
    
    offer_ids = fields.One2many("est.property.offer","property_type_id")
    offer_count = fields.Integer(compute="_compute_count")

    @api.depends("offer_ids")
    def _compute_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
