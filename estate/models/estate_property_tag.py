from odoo import fields, models


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    # --------------------------------------- Fields Declaration ----------------------------------
    # Basic Fields
    name = fields.Char("Tag", required=True)
