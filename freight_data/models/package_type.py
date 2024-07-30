from odoo import models, fields


class PackageType(models.Model):
    _name = "package.type"
    _description = "Package Type"

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    is_selection_ids = fields.Many2many(comodel_name='package.selection', string='Is')
    status = fields.Boolean(string='Status', default=True)
