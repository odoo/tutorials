from odoo import fields, models


class EventEvent(models.Model):
    _inherit = 'event.event'

    default_registration_limit = fields.Integer("Default registration limit", default=7, required=True)
