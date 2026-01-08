from odoo import models, fields, api


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    qty = fields.Float(string="Case Quantity", required=True)
    width = fields.Integer(string="Case Width (mm)", required=True)
    length = fields.Integer(string="Case Length (mm)", required=True)
    height = fields.Integer(string="Case Height (mm)", required=True)
    net_weight = fields.Float(string="Case Net Weight (Kg)", required=True)
    gross_weight = fields.Float(string="Case Gross Weight (Kg)", required=True)

    case_volume = fields.Float(
        string="Case Volume (m³)", compute="_compute_case_volume", readonly=True
    )

    @api.depends("width", "length", "height")
    def _compute_case_volume(self):
        for rec in self:
            rec.case_volume = (rec.width * rec.length * rec.height) / 1000000000
