# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class User(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        string="Properties",
        comodel_name="estate.property",
        inverse_name="salesperson_id",
        domain="[('state', 'in', ['new', 'offer_received'])]"
    )
