from odoo import models, fields


class ServiceScope(models.Model):
    _name = "service.scope"
    _description = "this is service scope"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    status = fields.Boolean(string='Status', default=True)
