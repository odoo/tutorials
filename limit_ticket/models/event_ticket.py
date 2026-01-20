from odoo import fields, models


class EventTicket(models.Model):
    _inherit = 'event.event.ticket'

    max_per_reg = fields.Integer(string='Max per registration',
        help='Define the maximum number of tickets allowed per registration',
        default=9
    )

    _sql_constraints = [
        ('max_per_registration_check', 'CHECK(max_per_reg > 0)', 'Number of max tickets per registration must be positive')
    ]
