from odoo import models,fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"

    name = fields.Char('Property Tag', required=True)
    