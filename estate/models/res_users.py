from odoo import models
from odoo.fields import One2many


class InheritedUser(models.Model):
    _inherit = "res.users"

    property_ids = One2many(
        comodel_name='estate.property',
        inverse_name='salesman_id',
        domain="[('state', 'not in', ('sold', 'canceled'))]"
    )
