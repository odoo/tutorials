# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EditSubProductLine(models.TransientModel):
    _name = 'edit.sub.product.line'
    _sql_constraints = [
        ('check_quantity', "CHECK(quantity >= 0)", "The quantity cannot be negative."),
        ('check_price_unit', "CHECK(price_unit >= 0.0)", "The unit price cannot be negative.")
    ]

    quantity = fields.Integer(string="Quantity", required=True, default=0)
    price_unit = fields.Float(string="Unit Price", required=True)

    product_id = fields.Many2one(comodel_name='product.product', required=True, ondelete='cascade')
    edit_sub_product_id = fields.Many2one(comodel_name='edit.sub.product', required=True, ondelete='cascade')
