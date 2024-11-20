# -*- coding: utf-8 -*-
# licence

from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tags"
    # _order = "sequence"

    name = fields.Char('Tag', required=True, translate=True)
    description = fields.Text('Tag description')