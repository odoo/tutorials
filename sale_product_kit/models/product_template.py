# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, Command, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean(string="Is Kit")

    sub_product_ids = fields.Many2many(
        comodel_name='product.product',
        string="Sub-Products",
        help="Products that are part of this kit product.",
        domain=[
            ('sale_ok', '=', True),
            ('type', '!=', 'combo'),
            ('is_kit', '=', False),
        ],
    )

    @api.constrains('is_kit')
    def _check_not_sub_product(self):
        kit_products = self.filtered(lambda template: template.is_kit)
        if kit_products:
            existing_kits = self.env['product.template'].search([('sub_product_ids', 'in', kit_products.mapped('product_variant_ids').ids)])
            if existing_kits:
                raise ValidationError(_("A product cannot be a kit if it is already a sub-product of another kit."))

    @api.constrains('is_kit', 'sub_product_ids')
    def _check_sub_product_ids_not_empty(self):
        if any(template.is_kit and not template.sub_product_ids for template in self):
            raise ValidationError(_("A kit product must contain at least one sub-product."))

    @api.constrains('sub_product_ids')
    def _check_sub_product_not_itself(self):
        if any(template.id in template.sub_product_ids.ids for template in self):
            raise ValidationError(_("A kit product can't be a sub-product of itself."))

    @api.constrains('sub_product_ids')
    def _check_sub_product_is_sellable(self):
        if any(not all(template.sub_product_ids.mapped('sale_ok')) for template in self):
            raise ValidationError(_("A kit product can only contain sellable sub-products."))

    @api.constrains('sub_product_ids')
    def _check_sub_product_not_kit(self):
        if any(template.is_kit and any(template.sub_product_ids.mapped('is_kit')) for template in self):
            raise ValidationError(_("A kit product cannot have a kit sub-product."))

    @api.constrains('sub_product_ids')
    def _check_sub_product_not_duplicate(self):
        if any(len(set(template.sub_product_ids.ids)) != len(template.sub_product_ids) for template in self):
            raise ValidationError(_("Kit product can't contain duplicate sub-products."))

    @api.constrains('sub_product_ids')
    def _check_sub_product_not_combo(self):
        if any('combo' in template.sub_product_ids.mapped('type') for template in self):
            raise ValidationError(_("A sub-product can't be of type combo."))

    def write(self, vals):
        for template in self:
            if ('is_kit' in vals) and not vals.get('is_kit') and template.sub_product_ids:
                vals['sub_product_ids'] = [Command.clear()]
        return super().write(vals)
