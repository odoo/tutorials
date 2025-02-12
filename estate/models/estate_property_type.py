from odoo import fields, models 

class Estate_Property_Type (models.Model):
    _name = "estate_property_type_model"
    _description = "This is a property type model"

    _order = "sequence, name"
    sequence = fields.Integer('Sequence', default=1)
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate_model", "property_type_id")
    
    _sql_constraints = [
        ("check_type_name", "UNIQUE(name)", "type name should be unique")
    ]