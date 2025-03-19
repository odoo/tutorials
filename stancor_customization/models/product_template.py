# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit="product.template"

    wt_per_mt = fields.Float(string="Wt./Mtr.")
    wt_per_pc = fields.Float(string="Wt./PCs.")

    @api.constrains('wt_per_mt', 'wt_per_pc')
    def _check_conversion_factors(self):
        for record in self:
            if record.wt_per_mt <= 0 and record.wt_per_mt is not False:
                raise ValidationError("Weight per meter must be positive")
            if record.wt_per_pc <= 0 and record.wt_per_pc is not False:
                raise ValidationError("Weight per piece must be positive")