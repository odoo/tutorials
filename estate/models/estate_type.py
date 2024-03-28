from odoo import api, fields, models


class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "A property's type"
    _order = "sequence, name"

    _sql_constraints = [
        ("check_name", "unique(name)", "A property type's name must be unique"),
    ]

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Associated Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Associated Offers")
    offer_count = fields.Integer("Associated Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.write({"offer_count": len(record.offer_ids)})
