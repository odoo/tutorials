from odoo import models, fields

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "All tags applicable to estate properties"

    name = fields.Char(name = "Tag name", required = True)
