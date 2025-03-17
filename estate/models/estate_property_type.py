from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence, name"

    name = fields.Char(required = True)
    sequence = fields.Integer("Sequence", default=1)
    sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property type name must be unique.')
    ]

    property_ids = fields.One2many("estate.property", "property_type_id", string = "Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offers", string="Offers count")

    @api.depends("offer_ids")
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
class PropertyTypeLine(models.Model):
    _name = "estate.property.type.line"
    _description = "Real estate property type line"

    model_id = fields.Many2one("estate.property.type")
    name = fields.Char("Title")
    expected_price = fields.Float("Expected Price")
    state = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled")
    ], string="Status", required=True, copy=False, default="new")
