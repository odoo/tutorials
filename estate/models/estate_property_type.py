from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)

    _check_name = models.Constraint("UNIQUE(name)", "Name must be unique.")

    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )


class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Property Type Line"

    model_id = fields.Many2one("estate.property.type")
    name = fields.Char()
    expected_price = fields.Char()
    state = fields.Char()
