from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"

    name = fields.Char("Tag Name", required=True, help="Property Tags")
    