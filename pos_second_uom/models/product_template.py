# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_categ_id = fields.Many2one(comodel_name="uom.uom", string="UOM category", related="uom_id.category_id", store=True)
    pos_second_uom_id = fields.Many2one(comodel_name="uom.uom", string="Second UOM", domain="[('category_id', '=', uom_categ_id),  ('id', '!=', uom_id)]")
