from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate_tags"
    _description = "This is to say that this is the description of the Property Tags"

    name = fields.Char("Property Tags", required=True)
