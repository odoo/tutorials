from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char("Type", required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer(help="Used to order list.")

    _name_uniq = models.Constraint(
        "unique (name)",
        "A property type name must be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_assign_type(self):
        active_ids = self.env.context.get('active_ids')

        if active_ids and len(active_ids) > 1:
            raise UserError(
                self.env._("Select any one type to assign it to properties")
            )

        action = {
            "name": self.env._("Send"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "estate.assign.type.wizard",
            "target": "new",
            "context": {"default_property_type_id": self.id},
        }

        return action
