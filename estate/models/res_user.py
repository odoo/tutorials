from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='sell_person_id',
        string='Properties',
        domain="[('state', '=', 'available')]"
    )
