from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    name = fields.Char('Property Tag', required=True)
    _description =  "property tag description"

    # DB Constraints
    _sql_constraints = [
        ("check_tag_name_is_unique", "UNIQUE(name)", "This tag name already exists!"),
    ]