from odoo import fields, models, api


class Type(models.Model):
    _name = "estate.property.type"
    _description = "Type of property of Estate"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _uniq_name = models.Constraint(
        "unique(name)",
        "A Type name should be unique.",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
