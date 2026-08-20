from odoo import models, fields, api


class Users(models.Model):

    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="seller_id"
    )

    available_property_ids = fields.One2many(
        comodel_name="estate.property",
        compute="_compute_available_properties"
    )

    @api.depends("property_ids")
    def _compute_available_properties(self):
        for user in self:
            user.available_property_ids = user.property_ids.filtered(
                lambda property: property.state in ["new", "offer_received"]
            )
