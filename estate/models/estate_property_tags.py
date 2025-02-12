from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Property Tags"
    _order = "name asc"

    name = fields.Char(string="Property Tags" , required = True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)','Property tag names must be unique.')]
    