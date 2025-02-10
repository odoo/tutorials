from odoo import models, fields,api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "sequence, name asc"
    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "The property type name must be unique!")
    ]

    name = fields.Char("name", required=True)
    property_ids = fields.One2many('estate.property','property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
        store=True
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
