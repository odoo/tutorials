from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.translate import _


class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "An offer for a property"
    _order = "price DESC"

    # Description
    price = fields.Float()
    status = fields.Selection([
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    _sql_constraints = [
        ('check_price', 'CHECK(price>0)', "The price of the offer should be strictly positive")
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = (fields.Date.to_date(offer.create_date) or fields.Date.today()) + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            create = offer.create_date or fields.Date.today()
            if isinstance(create, datetime):
                create = create.date()
            offer.validity = (offer.date_deadline - create).days if offer.date_deadline else 0

    @api.constrains('status')
    def _check_selling_price(self):
        for offer in self:
            if offer.status == 'accepted' and offer.property_id.expected_price:
                min_price = offer.property_id.expected_price * 0.9
                if float_compare(offer.price, min_price, precision_digits=2) < 0:
                    raise ValidationError(_("The offer price cannot be lower than 90 percent of the expected price."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            if property_id:
                property = self.env['estate.property'].browse(property_id)

                # Update property state if it's new
                if property.state == 'new':
                    property.state = 'received'

                # Validate price against existing offers
                existing_prices = property.offer_ids.mapped('price')
                if existing_prices:
                    best_offer = max(existing_prices)
                    new_offer_price = vals.get('price', 0)
                    if new_offer_price < best_offer:
                        raise UserError(_("The offer is lower than the current best offer."))

        return super().create(vals_list)

    def action_set_refused(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError(_("Why you wanna cancel something sold fam?"))
            offer.status = 'refused'

    def action_set_accepted(self):
        for offer in self:
            if offer.status == 'refused':
                raise UserError(_("you already denied the offer :'("))

            if offer.property_id.state == 'sold' or offer.property_id.state == 'accepted':
                raise UserError(_("you already accepted an offer :'("))
            offer.status = 'accepted'

            # set all other offers to refused?
            offer.property_id.state = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
