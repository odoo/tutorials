from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta


class EstatepropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offers"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
    selection=[
        ('accepted', "Accepted"),
        ('refused', "Refused"),
    ],
    copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Property Type",
        store=True)
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity,
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity,
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline -
                    record.create_date.date()
                ).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("This property is already sold!")
            if 'accepted' in record.property_id.offer_ids.mapped('status'):
                raise UserError("An offer has already been accepted!")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'

            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = "refused"
            return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            if not property_id:
                continue
            estate_property = self.env['estate.property'].browse(property_id)
            if estate_property.offer_ids:
                max_existing_offer = max(estate_property.offer_ids.mapped('price'))
                if vals.get('price', 0) < max_existing_offer:
                    raise UserError(
                    f"Your offer ({vals.get('price')}) is lower than "
                    f"an existing offer ({max_existing_offer}). Please raise your offer."
                    )
            estate_property.state = 'offer_received'
        return super().create(vals_list)

    suspicious_offer = fields.Boolean(string="Suspicious Offer", compute="_compute_is_suspicious_offer", store=False)

    @api.depends('partner_id', 'create_date')
    def _compute_is_suspicious_offer(self):
        all_offers = self.env['estate.property.offer'].search([])

        for record in self:
            if record.create_date:
                same_partner = all_offers.filtered(lambda offer: offer.partner_id == record.partner_id)

                def within_5_mins(offer):
                    if offer.create_date:
                        diff = abs(offer.create_date - record.create_date)
                        return diff <= timedelta(minutes=5)

                suspicious_window = same_partner.filtered(within_5_mins)
                record.suspicious_offer = len(suspicious_window) >= 3
            else:
                record.suspicious_offer = False
