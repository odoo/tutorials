# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_ids = fields.One2many(related='uom_id.category_id.uom_ids')
    website_uom_id = fields.Many2one(comodel_name='uom.uom', string='Website Uom', domain= "[('id', 'in', uom_ids)]", required=True, default=lambda self: self._get_default_uom_id())
    change_qty = fields.Float(string="Change Quantity", store=True, compute="_compute_change_qty", default=1)

    @api.depends('uom_id', 'website_uom_id')
    def _compute_change_qty(self):
        for product in self:
            if product.uom_id and product.website_uom_id:
                product.change_qty = product.uom_id.factor / product.website_uom_id.factor
            else:
                product.change_qty = 1

    @api.onchange('uom_id')
    def _onchange_uom_id_update_website_uom_id(self):
        for product in self:
            if product.uom_id and product.uom_id.category_id != product.website_uom_id.category_id:
                product.website_uom_id = product.uom_id

    @api.constrains('uom_id', 'website_uom_id')
    def _check_uom_id_is_bigger_website_uom_id(self):
        for product in self:
            if product.uom_id.factor < product.website_uom_id.factor:
                raise ValidationError(_("Website Uom should be bigger than or equal to base Uom"))

    @api.model
    def get_change_qty_from_product_id(self, product_id):
        return self.env['product.product'].browse(product_id).product_tmpl_id.change_qty
