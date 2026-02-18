from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)

    @api.constrains('name')
    def _check_name_unique(self):
        for record in self:
            # Recherche d'autres tags avec le même nom
            existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing:
                raise ValidationError("The property tag name must be unique.")
