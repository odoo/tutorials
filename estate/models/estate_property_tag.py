from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Tag Name", required=True, index=True)
    property_type = fields.Char(string="Property Type")

    @api.constrains("name")
    def _check_unique_name(self):
        for record in self:
            existing_tag = self.search(
                [("name", "=", record.name), ("id", "!=", record.id)]
            )
            if existing_tag:
                raise ValidationError("Tag name must be unique!")


                
