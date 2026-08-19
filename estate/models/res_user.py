from odoo import fields, models


class User(models.Model):
    _inherit = "res.users"

    # Foreign fields

    property_ids = fields.One2many(
        "estate.property",
        "seller_id",
    )

    # Computed fields

    available_property_ids = fields.One2many(
        "estate.property", compute="_compute_filtered_properties"
    )

    def _compute_filtered_properties(self):
        for record in self:
            record.available_property_ids = record.property_ids.filtered(
                lambda x: x.state not in ("sold", "cancelled")
            )
