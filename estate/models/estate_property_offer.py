from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price_strictly_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'cancelled':
                raise UserError(self.env._("You cannot accept an offer on a cancelled property."))
            if offer.property_id.state in ('offer_accepted', 'sold'):
                raise UserError(self.env._("An offer has already been accepted for this property."))
            offer.state = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            offer.state = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = [vals['property_id'] for vals in vals_list]
        properties = self.env['estate.property'].search([('id', 'in', property_ids)])
        properties_by_id = {prop.id: prop for prop in properties}

        for vals in vals_list:
            property_record = properties_by_id[vals['property_id']]
            if float_compare(vals.get('price', 0.0), property_record.best_price, precision_rounding=0.01) < 0:
                raise UserError(self.env._(
                    "The offer must be higher than the existing offers (%s).",
                    property_record.best_price,
                ))
            if property_record.state == 'new':
                property_record.state = 'offer_received'
        return super().create(vals_list)
