from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _rec_names_search = ["name", "code"]
    _order = "sequence,name"

    name = fields.Char(required=True, string="Property Type", translate=True)
    code = fields.Char(string="Code")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(default=1)

    _unique_name = models.Constraint("UNIQUE(name)", "The name of the property type must be unique.")

    @api.depends("name", "code")
    def _compute_display_name(self):
        for record in self:
            record.display_name = (
                f"{record.name} [{record.code}]" if record.code else record.name
            )
