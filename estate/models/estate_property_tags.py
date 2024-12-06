
from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property tags Table"

    name = fields.Char('Name', required=True)