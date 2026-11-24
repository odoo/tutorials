from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"
    _order = 'price desc'

    price = fields.Float('Price', digits=(12, 2), required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    validity_days = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one("res.partner", string='Buyer', required=True)
    property_id = fields.Many2one("estate.property", required=True, readonly=True)
    property_status = fields.Selection(related="property_id.state")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _check_price = models.Constraint(
        "CHECK(price >= 0)",
        "The offer's price has to be positive."
    )

    def action_offer_accepted(self):
        for record in self:
            if record.property_id.state in ['sold', 'cancelled']:
                raise exceptions.UserError('This property is already sold or has been cancelled!')
            if record.property_id.state in ['offer_accepted']:
                raise exceptions.UserError('An offer has already been accepted.')
            else:
                record.status = 'accepted'
                record.property_id.state = 'offer_accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id

                # for offers in record.property_id.offer_ids:
                #     if offers.id != record.id:
                #         offers.status = 'refused'
                (record.property_id.offer_ids - record).write({'status': 'refused'})
        return True

    def action_offer_refused(self):
        for record in self:
            if record.property_id.state in ['sold', 'cancelled']:
                raise exceptions.UserError('This property is already sold or has been cancelled!')
            else:
                record.status = 'refused'
        return True

    @api.depends('validity_days', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date or fields.Date.today()) + relativedelta(days=record.validity_days)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() or fields.Date.today()
            if record.date_deadline:
                delta_dates = record.date_deadline - start_date
                record.validity_days = delta_dates.days
