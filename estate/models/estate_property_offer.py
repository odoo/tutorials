from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"
    _order = 'price desc'

    price = fields.Float('Price', digits=(12, 2), required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    validity_days = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    buyer_id = fields.Many2one("res.partner", string='Buyer', required=True)
    property_id = fields.Many2one("estate.property", required=True, readonly=True)
    property_status = fields.Selection(related="property_id.state", readonly=False)
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer's price has to be positive."
    )

    @api.depends('validity_days', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            start_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.date_deadline = fields.Date.add(start_date, days=record.validity_days)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            if record.date_deadline:
                delta_dates = record.date_deadline - start_date
                record.validity_days = delta_dates.days

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = {val['property_id'] for val in vals_list}
        property_records = self.env['estate.property'].browse(property_ids)
        best_prices = {prop.id: prop.best_price for prop in property_records}
        for offer in vals_list:
            prop_id = offer['property_id']
            if best_prices[prop_id] >= offer['price']:
                raise UserError(self.env._('The offer has to be greater than %.2f', best_prices[prop_id]))
            best_prices[prop_id] = offer['price']

        res = super().create(vals_list)
        res.filtered(lambda p: p.property_status == 'new').property_status = 'offer_received'
        return res

    def action_offer_accepted(self):
        for record in self:
            if record.property_id.state in ['sold', 'cancelled']:
                raise UserError(self.env._('This property is already sold or has been cancelled!'))
            if record.property_id.state in ['offer_accepted']:
                raise UserError(self.env._('An offer has already been accepted.'))

            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.buyer_id
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
            (record.property_id.offer_ids - record).status = 'refused'

    def action_offer_refused(self):
        for record in self:
            if record.property_id.state in ['sold', 'cancelled']:
                raise UserError(self.env._('This property is already sold or has been cancelled!'))
            record.status = 'refused'
