from odoo import api, fields, models


class EstatePropertyTypeModel(models.Model):
    _name = "estate_property_type"
    _description = "The type of an estate"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many("estate_property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate_property_offer", "property_type_id")
    offer_count = fields.Integer("Number of offers", compute="_compute_total_offers")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'A property tag name must be unique',
    )

    @api.depends("offer_ids")
    def _compute_total_offers(self):
        for property_type in self:
            property_type.offer_count = len(property_type.property_ids.mapped("offers_ids"))

    def action_view_offer(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "estate_property_offer",
            "name": "List Offers",
            "view_mode": "list",
            "domain": [('property_type_id', '=', self.id)],
            "context": {"default_property_id": False},
        }
