from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence desc"

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    property_ids = fields.Many2many(
        "estate.property",
    )

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id',
                                string="Offers")

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    _sql_constraints = [
        ('unique_name', 'unique(name)',
         'Types should have unique names.'),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for val in self:
            val.offer_count = len(val.offer_ids)
