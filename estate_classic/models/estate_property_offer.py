from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate_classic.property.offer"
    _description = "Property offer for an estate"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_classic.property", required=True)

    create_date = fields.Date(default=lambda self: self._get_current_day())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_validity_date", inverse="_inverse_validity_date")

    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        ('check_price_value', 'CHECK(price > 0)',
         'The offer price must be strictly positive.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            offered_property = self.env['estate_classic.property'].browse(vals['property_id'])
            if offered_property.state == 'sold':
                raise UserError("You cannot create an offer for a sold property.")
            if vals.get("price", 0.0) < offered_property.best_offer:
                raise UserError("You cannot create an offer with a lower amount than an existing offer.")
            if offered_property.state == 'new':
                offered_property.state = 'offer_received'
        return super().create(vals_list)

    @api.depends("create_date", "validity")
    def _compute_validity_date(self):
        for record in self:
            if record.create_date:
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
                UserError("This property cannot be bought by two people at the same time")

    def action_refuse_offer(self):
        self.status = "refused"

    def _get_current_day(self):
        return fields.Date.today()
