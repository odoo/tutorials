from odoo import api, fields, models

class EventEvent(models.Model):
    _inherit = "event.event"

    seats_max_per_buyer = fields.Integer(
        string='Max Tickert Per Buyer',
        help="Define the number of tickets single user can buy. If Set to 0 "
             "single user can buy all available tickets."
    )
