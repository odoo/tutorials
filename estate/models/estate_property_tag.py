# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real Estate Property Tag"
    _explanation = "Defines a real estate property tag"
    _order = "name"

    name = fields.Char('Property Tag', required=True)
