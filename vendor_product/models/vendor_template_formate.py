from odoo import fields, models


class VendorTemplateFormate(models.Model):
    _name = 'vendor.template.formate'

    file_header = fields.Char(string="File Header")
    odoo_field = fields.Many2one(comodel_name='ir.model.fields', domain=[('model', '=', 'product.product')], string="Odoo Field", required=True, ondelete="cascade")
    sequence = fields.Integer(string="Sequence", default=1)
    template_id = fields.Many2one('vendor.product.template', required=True)
