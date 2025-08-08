from odoo import fields, models


class InheritedUserModel(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='estate.property',
        string="Properties",
        inverse_name='salesman_id',
        domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]")
