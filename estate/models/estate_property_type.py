from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate properties types"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_id")
    line_ids = fields.One2many("estate.property.type.line", "model_id")
    sequence = fields.Integer(default=1, help="Used to order stages, lower is better")
    offers_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offers_ids")
    def _compute_total(self):
        for record in self:
            record.offer_count = len(record.offers_ids)

    _sql_constraints = [
        ("check_type_name_unique", "UNIQUE(name)",
         "The type name should be unique.")
    ]


class EstatePropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Estate properties types Line"

    model_id = fields.Many2one("estate.property.type")
    title = fields.Char(related="model_id.property_ids.name")
    expected_price = fields.Float(related="model_id.property_ids.expected_price")
    status = fields.Selection(related="model_id.property_ids.state")
    sequence = fields.Integer(default=1, help="Used to order stages, lower is better")
