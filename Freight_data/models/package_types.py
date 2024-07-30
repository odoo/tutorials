from odoo import models, fields

class PackageTypes(models.Model):
    _name = 'package.types'
    _description = 'Package Type'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    # is_option = fields.Selection(
    #     selection=[
    #     ('lcl', 'LCL'),
    #     ('air', 'AIR')
    # ], string='Is', required=True)
    freight_is_package_id = fields.Many2many("freight.is.package", string="Is option")
    status = fields.Boolean(string='Status', default=True)
