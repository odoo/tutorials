import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.orm.utils import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offers'
    _order = 'price desc'

    deadline = fields.Date()
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    price = fields.Float()
    property_id = fields.Many2one(comodel_name='estate.property', readonly=True, required=True, ondelete='cascade')
    property_type = fields.Char(related='property_id.property_type_id.type')
    property_type_id = fields.Many2one(related='property_id.property_type_id')
    status = fields.Selection(
        [
            ('refused', "Refused"),
            ('accepted', "Accepted")
        ],
        copy=False
    )
    validity = fields.Integer(compute="_compute_validity", inverse="_inverse_deadline", default=7)

    _check_offer_price = models.Constraint(
        'CHECK (price > 0)',
        "Offer price should be positive"
    )

    @api.depends('deadline')
    def _compute_validity(self):
        for offer in self:
            offer.validity = (offer.deadline - offer.create_date.date()).days if offer.deadline and offer.create_date else 7

    @api.depends('validity')
    def _inverse_deadline(self):
        for offer in self:
            start_date = offer.create_date.date() if offer.create_date else fields.Date.context_today(offer)
            offer.deadline = start_date + datetime.timedelta(days=offer.validity)

    @api.model
    def create(self, val_list):
        for val in val_list:
            current_price = val.get('price', 0)
            properties = self.env['estate.property'].browse(val.get('property_id'))
            highest_offer = max(properties.mapped('offer_ids.price')) if properties.offer_ids else 0
            if val.get('price') < highest_offer:
                raise UserError(f"Offer price Rs.{current_price} is less than {highest_offer}!")
        return super().create(val_list)

    def _refuse_remaining_offers(self, offer_id, all_offers):
        """
        Helper method to refuse all offers except for a specific one.
        """
        for offer in all_offers:
            if offer.id != offer_id:
                offer.status = 'refused'

    def offer_accepted(self):
        """
        Finalizes the acceptance of a specific offer.

        This method:
        1. Validates that the property isn't already accepted.
        2. Refuses all other competing offers for the same property.
        3. Sets the offer status to 'accepted'.
        4. Updates the property with the buyer, selling price, and 'offer_accepted' state.
        """
        self.ensure_one()
        property = self.property_id
        if property.state == 'offer_accepted' and self.status == 'accepted':
            raise ValidationError("Property already accepted!")
        remaining_offers = property.offer_ids - self
        remaining_offers.write({
            'status': 'refused'
        })
        self.status = 'accepted'
        property.write({
            'buyer_id': self.partner_id,
            'selling_price': self.price,
            'state': 'offer_accepted',
        })
        return True

    def offer_refused(self):
        """
        Sets the status of the selected offers to 'refused'.

        Iterates through the recordset to ensure no offer is already refused
        before updating the status.
        """
        for offer in self:
            if offer.status == 'refused':
                raise UserError("Property already refused!")
            offer.status = 'refused'
        return True

    def _cron_refuse_offer(self):
        now = fields.Datetime.now()
        offers = self.search([
            ('deadline', '<=', now)
        ])
        for offer in offers:
            offer.status = 'refused'
