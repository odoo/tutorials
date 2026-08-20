from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag, i.e. simple boolean characteristics of the estate outside the normal properties"

    name = fields.Char(required=True)
    visual_code = fields.Char(required=True, help="Visual character for purpose of brief visualization")
