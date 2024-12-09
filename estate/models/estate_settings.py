from odoo import models, fields

class EstateSettings(models.Model):
    _name = 'estate.settings'
    _description = 'Estate Settings'

    default_property_type = fields.Char(string="Default Property Type")
    enable_notifications = fields.Boolean(string="Enable Notifications")

