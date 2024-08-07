from odoo import models, fields


class estate_property_tag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tag"
    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_tag','UNIQUE(name)','Property Tag name must be unique')
    ]
