from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string="Properties"
    )

    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id'
    )

    offer_count = fields.Integer(compute="_compute_offer_count")

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

