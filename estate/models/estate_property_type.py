from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )

    name = fields.Char(string="Name", required=True, index=True)
    expected_price = fields.Float(string="Expected Price")

    @api.constrains("name")
    def _check_unique_name(self):
        for record in self:
            existing_type = self.search(
                [("name", "=", record.name), ("id", "!=", record.id)]
            )
            if existing_type:
                raise ValidationError("Property Type name must be unique!")
                