from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True, readonly=True)

    _check_offer_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be positive.',
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = (
                    offer.create_date.date()
                    + relativedelta(days=offer.validity)
                )
            else:
                offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (
                    offer.date_deadline
                    - offer.create_date.date()
                ).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price")
            property_rec = self.env["estate.property"].browse(property_id)

            # Prevent lower offer
            existing_prices = property_rec.offer_ids.mapped("price")
            if existing_prices and price < max(existing_prices):
                raise UserError("You cannot create an offer lower than an existing offer")

            # Set property state
            property_rec.state = "offer_received"

        offers = super().create(vals_list)

        for offer in offers:
            # Only create CRM lead if CRM module is installed
            if self.env['ir.module.module'].sudo().search([('name', '=', 'crm'), ('state', '=', 'installed')]):
                self.env['crm.lead'].create({
                    'name': offer.property_id.name,
                    'partner_id': offer.partner_id.id,
                    'expected_revenue': offer.price,
                    'type': 'lead',
                })
        return offers

    @api.constrains('property_id')
    def _check_property_state(self):
        for offer in self:
            if offer.property_id.state in ('sold', 'cancelled'):
                raise ValidationError("You cannot add an offer on a Sold or Cancelled property")

    def action_accept(self):
        for offer in self:
            property_rec = offer.property_id

            if property_rec.buyer_id:
                raise UserError("Property already accepted")

            other_offer = property_rec.offer_ids - offer
            other_offer.write({'status': 'refused'})

            offer.status = "accepted"
            property_rec.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
                'state': 'offer_accepted',
            })
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
