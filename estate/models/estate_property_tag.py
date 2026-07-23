from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "realestate.properties.tag"
    _description = "Real estate property tag"

    name = fields.Char("Name", required=True)
    property_tag_ids = fields.Char("id", required=True)
