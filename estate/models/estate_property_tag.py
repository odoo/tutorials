from odoo import fields, models

class EstatePropertyTag(models.Model):
    
    _name = "estate.property.tag"
    _description = "Estate property tag"

    name= fields.Char(string="Name", required=True)
    _sql_constraints= [
        ('tag_name_unique_check', 'UNIQUE(name)', 'Given Property tag already exist please choose unique property tag')
    ]