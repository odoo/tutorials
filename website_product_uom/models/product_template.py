# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_category_id = fields.Many2one('uom.category', compute="_compute_uom_category")
    website_uom_id = fields.Many2one(
        'uom.uom',
        string="Website UoM",
        domain="[('category_id', '=', uom_category_id)]",
        help="Unit of Measure used on the website.",
        default=lambda self: self.env.ref('uom.product_uom_unit'),
        required=True
    )

    @api.constrains('website_uom_id', 'uom_id')
    def _check_website_uom_category(self):
        for product in self:
            if product.website_uom_id and product.uom_id:
                if product.website_uom_id.category_id != product.uom_id.category_id:
                    raise ValidationError(_("The Website UoM must belong to the same category as the main UoM."))

    @api.depends('uom_id')
    def _compute_uom_category(self):
        for record in self:
            record.uom_category_id = record.uom_id.category_id

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        if self.website_uom_id and self.website_uom_id.category_id != self.uom_id.category_id:
            self.website_uom_id = False
            return {
                'warning': {
                    'title': _("Website UoM Reset"),
                    'message': _("The Website UoM belongs to a different category. It has been cleared. Please select a new one from the updated category.")
            }
        }
