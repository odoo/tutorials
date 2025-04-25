from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate: Type of Property"
    _order = "name asc"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property")
    sequence = fields.Integer("Sequence", default=1, help="Used to order stages.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self) -> None:
        for record in self:
            record.offer_count = len(record.offer_ids.filtered(lambda x: x.property_type_id.name == record.name))

    _sql_constraints = [("type_name_unique", "UNIQUE(name)", "A type with the same name already exists.")]
