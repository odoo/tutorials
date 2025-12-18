from odoo import models, fields


class building_tags_model(models.Model):
    _name = "estate.building_tags"
    _description = "Building Tags Model"

    name = fields.Char(required=True)
