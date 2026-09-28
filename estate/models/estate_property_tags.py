from typing import Required

from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tags'
    _description = "real estate property tag"

    name = fields.Char(required=True)