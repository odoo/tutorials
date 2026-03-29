from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "sequence,name"

    name = fields.Char(string="Property Category", required=True)
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offers")
    property_type_id = fields.Integer()
    sequence = fields.Integer(
        "sequence",
        default=1,
        help="Used in ordering property,often sold property types are displayed",
    )
    property_ids = fields.One2many("estate.property", "property_type_id")
    property_offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    _check_name_unique = models.Constraint(
        "unique(name)",
        "The Property type must be unique.",
    )

    @api.depends("property_offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.property_offer_ids)

    def action_view_offers(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [("property_type_id", "=", self.id)],
        }
