from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "test description 3"
    _order = "name"

    name = fields.Char(required=True, unique=True)
    color = fields.Integer("Color", default=0xFFFFFF)

    @api.constrains("name")
    def _check_unique_name(self):
        for record in self:
            # Check if the name already exists in other records (excluding the current one)
            existing_tag = self.search(
                [("name", "=", record.name), ("id", "!=", record.id)], limit=1
            )
            if existing_tag:
                raise ValidationError(
                    "The tag name must be unique. '%s' already exists." % record.name
                )
