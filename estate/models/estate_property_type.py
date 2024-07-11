from odoo import fields, models


class Estatepropertytype(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "sequence, name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Type",
    )
    related_property_count = fields.Integer(compute="_compute_property_count")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offer",
    )
    related_offer_count = fields.Integer(compute="_compute_offer_count")

    def _compute_offer_count(self):
        for record in self:
            record.related_offer_count = self.env["estate.property.offer"].search_count(
                [
                    ("property_type_id", "=", record.id),
                ]
            )

    def _compute_property_count(self):
        for record in self:
            record.related_property_count = self.env["estate.property"].search_count(
                [
                    ("property_type_id", "=", record.id),
                ]
            )

    def action_display_property(self):
        related_property_ids = (
            self.env["estate.property"]
            .search(
                [
                    ("property_type_id", "=", self.id),
                ]
            )
            .ids
        )
        return {
            "type": "ir.actions.act_window",
            "name": ("Properties"),
            "res_model": "estate.property",
            "views": [[False, "list"], [False, "form"]],
            "domain": [("id", "in", related_property_ids)],
        }

    _sql_constraints = [
        (
            "check_property_typename",
            "UNIQUE(name)",
            "Property Type Name must be unique",
        )
    ]
