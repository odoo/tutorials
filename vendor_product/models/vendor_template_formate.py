from odoo import fields, models


class VendorTemplateFormate(models.Model):
    _name = 'vendor.template.formate'

    file_header = fields.Char(string="File Header", required=True)
    odoo_field_id = fields.Many2one('ir.model.fields', string="Odoo Field", required=True, ondelete="cascade", domain=[('model', '=', 'product.product')])
    sequence = fields.Integer(string="Sequence", default=1)
    template_id = fields.Many2one('vendor.product.template', required=True)
