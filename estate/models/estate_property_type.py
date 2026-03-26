from odoo import api, models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Loại bất động Sản"

    name = fields.Char(string="Title", required=True)
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties"
    )
    sequence = fields.Integer("Sequence", default=1)
    _order = "sequence, name"
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count", default=1)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
    ('unique_type_name', 'UNIQUE(name)', 'Tên loại không được trùng')
]
