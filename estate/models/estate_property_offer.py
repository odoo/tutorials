from datetime import timedelta
from odoo import api, fields, models

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    allowed_partner_ids = fields.Many2many(
        "res.partner",
        compute="_compute_allowed_partners",
        store=False
    )

    @api.depends('property_id')
    def _compute_allowed_partners(self):
        for record in self:
            partners = self.env['res.partner']
            if record.property_id:
                if record.property_id.event_id:
                    registrations = record.property_id.event_id.registration_ids.filtered(
                        lambda record: record.state == 'done'
                    )
                    partners |= registrations.mapped('partner_id')

                visits = record.property_id.visit_ids.filtered(
                    lambda record: record.state == 'done')
                partners |= visits.mapped('partner_id')

            record.allowed_partner_ids = partners

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    @api.model
    def create(self, vals_list):
        if self.env.user.has_group('estate.group_estate_manager'):
            raise UserError("Managers cannot create offers")

        for vals in vals_list:
            property_record = self.env['estate.property'].browse(vals.get('property_id'))
            partner_id = vals.get('partner_id')
            allowed_partners = self.env['res.partner']

            if property_record.event_id:
                registrations = property_record.event_id.registration_ids.filtered(
                    lambda r: r.state == 'done'
                )
                allowed_partners |= registrations.mapped('partner_id')

            visits = property_record.visit_ids.filtered(
                lambda v: v.state == 'done'
            )
            allowed_partners |= visits.mapped('partner_id')

            if partner_id not in allowed_partners.ids:
                raise UserError("Only attendees and visitors can create offers.")
            if property_record.state in ('offer_accepted', 'sold'):
                raise UserError("Cannot create new offer. An offer is already accepted.")
            if property_record.offer_ids:
                highest_price = max(property_record.offer_ids.mapped('price'))
                if vals.get('price') <= highest_price:
                    raise UserError("New offer must not cost less than the previous offers")

        offers = super().create(vals_list)
        for offer in offers:
            offer.property_id.state = 'offer_received'

        return offers

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ["cancelled", "sold"]:
                raise UserError("Cannot accept an offer for a cancelled or sold property")
            accepted_offers = record.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )
            other_offers = record.property_id.offer_ids.filtered(
            lambda offer: offer.id != record.id
            )
            other_offers.write({'status': 'refused'})
            if accepted_offers:
                raise UserError("an offer has already been accepted for this property")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.property_id.state in ["cancelled", "sold"]:
                raise UserError("Cannot modify offers for a sold or cancelled property")
            if record.status == "accepted":
                record.property_id.buyer_id = False
                record.property_id.state = "new"
            record.status = "refused"

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive."
    )
    
    @api.model
    def _cron_refuse_after_deadline(self):
        today = fields.Date.today()

        offers = self.search([
            ('date_deadline', '<', today),
            ('status', '!=', 'refused'),
        ])

        for offer in offers:
            offer.action_refuse()
