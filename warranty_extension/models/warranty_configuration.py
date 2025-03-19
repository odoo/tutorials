from odoo import models, fields, api


class WarrantyConfiguration(models.Model):
    _name = 'warranty.configuration'
    _description = 'Warranty Configuration'

    name = fields.Char(required=True, compute='_compute_name')
    product_tmpl_id = fields.Many2one('product.template', string="Product Template", required=True)
    year = fields.Integer(string="Year", required=True)
    percentage = fields.Float(string='Percentage', required=True)

    @api.depends('year')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.year} Year'
