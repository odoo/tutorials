# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string='Estate Property Tag', required=True)
