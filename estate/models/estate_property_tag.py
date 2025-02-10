from datetime import timedelta
from odoo import api, exceptions, fields, models
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Different Tags to describe the aesthetics of Property"
    
    name = fields.Char('Property Tag', required = True)
    #SQL Constraints
    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'The property tag name must be unique.')
    ]