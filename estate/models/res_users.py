from odoo import fields, models

class User(models.Model):
    #---------- Extension Inheritance ----------
    _inherit = "res.users"

    #---------------------------------------------------------------------
    # Relations
    #---------------------------------------------------------------------
    property_ids = fields.One2many("estate.property", "user_id", domain=["|", ("status", "=", "new"), ("status", "=", "offer_received")])
