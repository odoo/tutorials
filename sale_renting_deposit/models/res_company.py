# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class RentalCompany(models.Model):
    _inherit = "res.company"

    deposit_product = fields.Many2one(
        string="Deposit",
        help="This product will be used to add deposits in the Rental Order.",
        comodel_name="product.product",
    )
