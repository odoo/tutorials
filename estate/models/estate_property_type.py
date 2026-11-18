# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property test model'

    name = fields.Char(required=True)
    