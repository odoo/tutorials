from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools import _


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "price desc"

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity", default=7, help="Expressed in days")
    # validity = fields.Integer(string="Validity (Days)", compute="_inverse_date_deadline", inverse="_compute_date_deadline")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Estate Property Type",
        related="property_id.property_type_id",
        store=True
    )

    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'An offer price must be strictly positive.')
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(offer.create_date.date(), days=offer.validity)
            else:
                offer.date_deadline = fields.Date.add(fields.Date.today(), days=offer.validity)

    @api.depends("create_date", "date_deadline")
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                if offer.create_date:
                    delta = offer.date_deadline - offer.create_date.date()
                    offer.validity = delta.days
                else:
                    delta = offer.date_deadline - fields.Date.today()
                    offer.validity = delta.days

    def action_accept(self):

        property_ids = self.mapped('property_id.id')
        accepted_offers = self.env['estate.property.offer'].search([
            ('status', '=', 'accepted'),
            ('property_id', 'in', property_ids)
        ])
        accepted_offer_map = {offer.property_id.id: offer for offer in accepted_offers}

        for offer in self:
            if accepted_offer_map.get(offer.property_id.id):
                raise UserError("This property already has an accepted offer.")

            if offer.status == 'accepted':
                raise UserError("This offer was already accepted.")

            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.status = 'accepted'
        return True
    

    def action_refuse(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.buyer_id = None
                offer.property_id.selling_price = 0.0
            offer.status = 'refused'
        return True
    
    @api.model_create_multi
    def create(self, vals_list):

        vals_list = [vals for vals in vals_list if vals.get('property_id')]

        property = self.env['estate.property'].browse(vals_list['property_id'])

        highest_offer = self.search([
            ('property_id', 'in', vals_list['property_id'])
        ], order="price desc", limit=1)

        if highest_offer and vals_list['price'] <= highest_offer.price:
            raise UserError(_("The new offer must be higher than the existing offers."))

            if property.state == 'new':
                property.state = 'offer_received'

        return super(PropertyOffer, self).create(vals_list)

