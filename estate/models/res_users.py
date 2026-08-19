from odoo import models, fields, api


class Users(models.Model):

    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="seller"
    )

    available_properties = fields.One2many(
        comodel_name="estate.property",
        compute="_compute_available_properties"
    )

    # Probably overkill but domains don't seem to work here or in the view ?
    @api.depends("property_ids")
    def _compute_available_properties(self):
        for user in self:
            user.available_properties = user.property_ids.filtered(
                lambda property: property.state in ["new", "offer_received"]
            )
