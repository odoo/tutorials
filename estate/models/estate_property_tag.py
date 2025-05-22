from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description =  "property tag description"
    name = fields.Char('Property Tag', required=True)
    color = fields.Integer()

    # Ordering
    _order = "name asc"

    # DB Constraints
    _sql_constraints = [
        ("check_tag_name_is_unique", "UNIQUE(name)", "This tag name already exists!"),
    ]
