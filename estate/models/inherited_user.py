# Odoo Imports
from odoo import fields, models


class InheritedUser(models.Model):
    _inherit = 'res.users'

    # -----------------------------
    # Field Declarations
    # -----------------------------
    property_ids = fields.One2many(
        'estate.property',
        'sales_id',
        string='Properties',
        domain=[('state', 'in', ['new', 'offer_received'])],
        help='Properties assigned to this salesman with status New or Offer Received.'
    )
