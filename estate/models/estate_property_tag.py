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
        tag_list = (
            self.env["estate.property.tag"]
            .search([("id", "not in", self.id)])
            .mapped("name")
        )
        existing_tag_list = [word.lower() for word in tag_list]

        for record in self:
            if record.name.lower() in existing_tag_list:
                raise ValidationError("Tag already present")
