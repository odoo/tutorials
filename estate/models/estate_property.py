from odoo import models, fields


class RealEstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property model"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description", help="write the desc of this prop")
