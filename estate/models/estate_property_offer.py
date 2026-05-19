from datetime import date, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'
    _check_price = models.Constraint(
        'CHECK(price > 0)', "Offer price must be positive."
    )

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = (record.create_date or fields.Datetime.now()).date()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - base_date).days
            else:
                record.validity = 7

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env['estate.property'].browse(vals.get('property_id'))

            if property_record:
                if property_record.offer_ids:
                    highest_existing_offer = max(property_record.offer_ids.mapped('price'))

                    if vals.get('price', 0) < highest_existing_offer:
                        raise UserError(("The offer price cannot be lower than an existing offer of %s.") % highest_existing_offer)

                property_record.state = 'offer_received'

        return super().create(vals_list)

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state in ['sold', 'cancelled']:
                raise UserError("You cannot accept an offer for a property that is already sold or cancelled.")

            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("An offer has already been accepted for this property.")

            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'
        return True

    def action_reject_offer(self):
        self.status = "refused"
        return True
