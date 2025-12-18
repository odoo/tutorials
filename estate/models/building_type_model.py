from odoo import models, fields


class building_type_model(models.Model):
    _name = "estate.building_type"
    _description = "Building Type Model"

    name = fields.Char(required=True)
