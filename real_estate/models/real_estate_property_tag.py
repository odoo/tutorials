from odoo import fields, models

class RealEstateTag(models.Model):
    _name = 'real.estate.property.tag'
    _description = "Real estate Tags for Properties"

    name = fields.Char(string = "Name", required = True)

    #Sql constraints for Unique tag name
    _sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)', 'A property tag name must be unique')
    ]
