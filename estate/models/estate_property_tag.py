from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"

    name = fields.Char(string="Tag", required=True)

    # ch-11 ex-3
    _order = "name"
    
    # ch-10
    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'Property Tag Must be Unique')]
    
    # ch-11 ex-5
    color = fields.Integer(string="Color")