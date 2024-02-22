from odoo import fields, models


class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate tags."
    _order = "name asc"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('name_tag_unique',
         'unique(name)',
         'The name of the tag should be unique')]
