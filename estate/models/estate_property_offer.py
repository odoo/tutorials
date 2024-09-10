from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Offer by")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_date_deadline", inverse="_inverse_date_deadline")

    # date_deadline = {creation date} + {validity} days
    @api.depends("create_date", "validity")
    def _date_deadline(self):
        for record in self:
            # record.create_date is None before the record is created
            startingDate = record.create_date or fields.Date.today()

            record.date_deadline = fields.Date.add(startingDate, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days