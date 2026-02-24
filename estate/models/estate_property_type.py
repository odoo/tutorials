from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _rec_name = "bedrooms"

    name = fields.Char(string="Property Type", required=True)
    bedrooms = fields.Char(string="Bedrooms", required=True)

    _unique_name = models.Constraint(
        "UNIQUE(name)", "The property type name must be unique"
    )

    @api.depends("name", "bedrooms")
    def _compute_display_name(self):
        for record in self:
            if record.bedrooms:
                record.display_name = f"{record.name} ({record.bedrooms})"
            else:
                record.display_name = record.name
