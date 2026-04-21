from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of properties (f.e. house)"
    _order = "name"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(
        "Sequence",
        default=1,
        help="Used to order property types."
    )

    _check_unique = models.Constraint(
        "UNIQUE(name)"
    )

    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers for this property type",
    )

    offer_count = fields.Integer(
        string="Offers",
        compute="_compute_total_offers"
    )

    @api.depends("offer_ids")
    def _compute_total_offers(self):
        for record in self:
            record.offer_count = len(self.offer_ids)

    def action_view_offers(self):
        action = {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "target": "current",
            "view_mode": "list",
            "domain": [["property_type_id", "=", self.id]]
        }
        return action
