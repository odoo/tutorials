from odoo import api, fields, models


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"

    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    estate_property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Estate Property",
        required=True,
    )
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    property_name = fields.Char(related="estate_property_id.name")
    property_type_name = fields.Char(
        related="estate_property_id.estate_property_type_id.name",
    )
    property_price = fields.Float(related="estate_property_id.expected_price")
    property_postcode = fields.Char(related="estate_property_id.postcode")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for o in self:
            if o.create_date:
                o.date_deadline = fields.Date.add(
                    o.create_date,
                    days=o.validity,
                )
            else:
                o.date_deadline = fields.Date.add(fields.Date.today(), days=o.validity)

    def _inverse_date_deadline(self):
        for o in self:
            o.validity = (o.date_deadline - o.create_date.date()).days
