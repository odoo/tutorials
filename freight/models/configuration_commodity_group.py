from odoo import models, fields


class ConfigurationCommodityGroup(models.Model):
    _name = "configuration.commodity.group"
    _description = "this is Configuration Commodity Group"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    status = fields.Boolean(string='Status', default=True)
