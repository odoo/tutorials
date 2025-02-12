from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='salesman_id',
        string="Properties",
        help="List of properties assigned to this user as a salesperson"
    )
