from odoo import fields, models


class EstatePropertyType(models.Model):
    _name: str = "estate.property.type"
    _description: str | None = None
    _order = "name"

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    name: fields.Char = fields.Char()
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offers_count")

    _unique_name = models.Constraint(
        'unique (name)',
        "Type nmust be unique!",
    )

    def _compute_offers_count(self):
        return len(self.offer_ids)
