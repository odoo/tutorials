from odoo import fields, models



class EstatePropertyTag(models.Model):
    _name = "property.tags"
    _description = "Estate Property Tags"



    tags_of_property = fields.Char('Property tags', required=True)