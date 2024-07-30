from odoo import models, fields


class FreightPackageType(models.Model):
    _name = "freight.package.type"
    _description = "this is freight package type"

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    status = fields.Boolean(string='Status', default=True)

    is_air = fields.Boolean(string='Is Air')
    is_lcl = fields.Boolean(string='Is LCL')
