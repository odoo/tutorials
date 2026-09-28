from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price of a property must be positive.'
    )

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
        )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Type of property", store=True)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            if record.date_deadline:
                record.validity = (
                    record.date_deadline - fields.Date.to_date(create_date)
                ).days
            else:
                record.validity = 0

    def action_set_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id

            for offer in record.property_id.offer_ids:
                if offer != record:
                    offer.status = "refused"
        return True

    def action_set_refused(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals.get('property_id'))
            offer_price = vals.get('price', 0)

            for existing_offer in property_id.offer_ids:
                if offer_price <= existing_offer.price:
                    raise UserError(self.env._("You cannot create an offer with a price lower than another offer."))

        offers = super().create(vals_list)

        for offer in offers:
            offer.property_id.state = 'offer_received'

        return offers
