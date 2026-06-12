from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatepropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offers"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    suspicious_offer = fields.Boolean(string="Suspicious Offer", compute="_compute_is_suspicious_offer", store=False)

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.'
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    @api.depends('partner_id', 'create_date')
    def _compute_is_suspicious_offer(self):
        for record in self:
            if not record.create_date or not record.partner_id:
                record.suspicious_offer = False
                continue

            suspicious_offers_count = self.env['estate.property.offer'].search_count([
                ('partner_id', '=', record.partner_id.id),
                ('create_date', '>=', record.create_date - timedelta(minutes=5)),
                ('create_date', '<=', record.create_date + timedelta(minutes=5)),
            ])

            record.suspicious_offer = suspicious_offers_count >= 3

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

    def action_accept(self):
        if self.env.user.has_group('estate.group_estate_agent'):
            raise UserError("Agents can add offers but cannot accept them.")
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
        if self.env.user.has_group('estate.group_estate_agent'):
            raise UserError("Agents can add offers but cannot refuse them.")
        for record in self:
            record.status = 'refused'
        return True
