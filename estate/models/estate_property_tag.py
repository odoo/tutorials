from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "It is a estate property tag model"
    _order = "name desc"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    @api.constrains("name")
    def _check_unique_tag_name(self):
        if len(self) > 1:
            raise ValidationError(self.env._("Tag duplication not allowed"))
        tag_present = self.search_count(
            [("id", "!=", self.id), ("name", "=ilike", self.name)]
        )

        if tag_present:
            raise ValidationError(self.env._("A tag with this name already exists."))
