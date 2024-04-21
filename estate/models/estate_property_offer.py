""" A module defining an offer to buy a real estate property and the related behavior"""

from odoo import api, fields, models
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    """
    Represents an offer to buy a real estate property.
    """
    _name = "estate_property_offer"
    _description = "An offer to buy a real estate property"
    _sql_constraints = [
        ('check_positive_price', 'CHECK (price > 0)', 'The Price must be strictly positive'),
    ]
    _order = 'price desc'
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('Accepted', 'Accepted'),
            ('Refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate_property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    # No need to add creation_date to @api.depends, because the create date will never change.
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date if record.create_date else fields.Date.today(),
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            # No need to check whether record.create_date is present because the inverse function is called
            # when the record is saved, so the create date will be present.
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model
    def create(self, vals_list):
        Property = self.env['estate_property'].browse(vals_list['property_id'])
        if vals_list['price'] < min(Property.mapped('property_offer_ids.price'), default=vals_list['price']):
            raise UserError('The price given is lower than the price of an existing offer.')
        Property.state = "Offer Received"
        return super().create(vals_list)

    def action_accept(self):
        """
        On an offer being accepted, set the selling price and buyer of the real estate property.
        Set the state of the offer to Accepted and set the state of the property to Offer Accepted.
        """
        self.ensure_one()
        if "Accepted" in self.mapped('property_id.property_offer_ids.status'):
            raise UserError("There can only be one accepted offer")

        self.status = "Accepted"
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        self.property_id.state = "Offer Accepted"
        return True

    def action_refuse(self):
        """
        On an offer being refused, Set the state of the offer to refused.
        """
        self.ensure_one()
        self.status = "Refused"
        return True

