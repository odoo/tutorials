from datetime import timedelta
from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            start_date = fields.Date.to_date(
                offer.create_date) or fields.Date.today()
            offer.date_deadline = start_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                start_date = fields.Date.to_date(
                    offer.create_date) or fields.Date.today()
                offer.validity = (offer.date_deadline - start_date).days
            else:
                offer.validity = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals['property_id'])
            if prop.offer_ids:
                max_offer = max(prop.offer_ids.mapped('price'))
                if vals.get('price') < max_offer:
                    raise exceptions.UserError(
                        ("The offer must be higher than %.2f") % max_offer)
            prop.state = 'offer received'

        return super().create(vals_list)

    def action_accept(self):
        for offer in self:
            existing_accepted = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted')
            ])
            if existing_accepted:
                raise exceptions.UserError(
                    "An offer for this property has already been accepted.")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer accepted'

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
