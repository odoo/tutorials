from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"
    _rec_name = "id"

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )

    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "Property type name must be unique."
    )

    @api.depends("name", "create_date")
    def _compute_display_name(self):
        for record in self:
            if record.create_date:
                record.display_name = f"{record.name} ({record.create_date.date()})"
            else:
                record.display_name = record.name