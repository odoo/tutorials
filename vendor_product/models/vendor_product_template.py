from odoo import fields, models


class VendorProductTemplate(models.Model):
    _name = 'vendor.product.template'
    _description = 'Vendor Product template model'

    name = fields.Char(requierd=True, string="Name")
    vendor_id = fields.Many2one('res.partner', requierd=True)
    template_formate_ids = fields.One2many('vendor.template.formate', 'template_id', string="Vendor Template Formate")

    