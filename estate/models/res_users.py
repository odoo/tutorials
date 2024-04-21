from odoo import fields, models

class ResUser(models.Model):
    """
    Inherits from res.users to link a salesperson and the properties that they were able to sell.
    """
    _inherit = "res.users"

    property_ids = fields.One2many('estate_property', 'user_id', domain=[('state', 'in', ['New', 'Offer Received'])])
