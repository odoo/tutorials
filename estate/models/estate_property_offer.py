from odoo import fields, models
from odoo import api
from odoo import exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer for an estate"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    create_date = fields.Date(default=lambda self: self._get_current_day())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_validity_date", inverse="_inverse_validity_date")

    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        ('check_price_value', 'CHECK(price >= 0)',
         'The offer price must be strictly positive.')
    ]

    @api.depends("create_date", "validity")
    def _compute_validity_date(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_validity_date(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_accept_offer(self):
        for record in self:
            if not record.property_id.buyer_id:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = 'offer_accepted'
            else:
                exceptions.UserError("This property cannot be bought by two people at the same time")

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"

    def _get_current_day(self):
        return fields.Date.today()
