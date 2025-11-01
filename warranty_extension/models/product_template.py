from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    warranty_configuration_ids = fields.Many2many('warranty.configuration', string="Warranty Configurations")
    is_warranty = fields.Boolean(string='Is Warranty')
