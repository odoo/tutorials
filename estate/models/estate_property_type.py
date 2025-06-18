from odoo import fields,models,api


class estate_property_type(models.Model):
    # Private attributes
    _name = "estate.property.type"
    _description = "Estate property type file"
    _order = "sequence, name"

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique"),
    ]

    # Fields declaration
    name = fields.Char('Name',required=True, translate=True, default='Unknown')
    property_ids = fields.One2many("estate.property","property_type_id",string="Property")
    offer_ids = fields.One2many("estate.property.offer","property_type_id",string="Property")
    offer_count = fields.Integer("Offer counted",compute="_compute_offer_count")

    sequence = fields.Integer('Sequence', default=1)

    # compute and search fields
    @api.depends("offer_ids.price")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count=len(record.offer_ids.mapped("price")) if record.offer_ids else 0