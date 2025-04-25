from odoo import api, models, fields
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = val.get('property_id')
            price = val.get('price')

            prop = self.env['estate.property'].browse(property_id)

            existing_offer_prices = prop.offers_ids.mapped('price')
            if existing_offer_prices:
                max_existing_offer = max(existing_offer_prices)
                if float_compare(price, max_existing_offer, precision_digits=2) < 0:
                    raise UserError("Cannot create an offer with a price lower than an existing offer")

            if prop.state == 'new':
                prop.write({'state': 'offer_received'})

        new_offer = super(EstatePropertyOffer, self).create(vals)
        return new_offer

    def action_accept(self):
        for record in self:
            accepted_offers = record.property_id.offers_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offers:
                raise UserError("Another offer has already been accepted for this property.")
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                base_date = record.create_date.date()
            else:
                base_date = fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                base_date = record.create_date.date()
            else:
                base_date = fields.Date.today()
            record.validity = (record.date_deadline - base_date).days
