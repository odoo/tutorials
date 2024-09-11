from odoo import _, api, fields, models
from odoo.exceptions import UserError

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

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.'),
    ]

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


    # actions
    def action_accept_offer(self):
        self.ensure_one()
        self.status = 'Accepted'
        if self.property_id.selling_price == 0.0:
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price
        else:
            raise UserError(_('You cannot accept multiple offers at the same time.'))
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        if self.status == 'Accepted': # if previously accepted, reset offer values
            self.property_id.selling_price = 0.0
            self.property_id.buyer_id = None
        self.status = 'Refused'
        return True