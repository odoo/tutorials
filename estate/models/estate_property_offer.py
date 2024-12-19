from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string="Type",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Datetime.today()
            record.date_deadline = fields.Datetime.add(
                record.create_date, days=record.validity
            )
            print("Hi there")

    def _inverse_date_deadline(self):
        for record in self:
            print((record.date_deadline - record.create_date.date()).days)
            record.validity = (record.date_deadline - record.create_date.date()).days
