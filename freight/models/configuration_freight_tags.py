from odoo import models, fields


class ConfigurationFreightTags(models.Model):
    _name = "configuration.freight.tags"
    _description = "this is configuration freight tags"

    name = fields.Char(string="Name")
    status = fields.Boolean(string='Status', default=True)
