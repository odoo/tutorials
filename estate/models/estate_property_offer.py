
from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


# estate.property.offer model
class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer database table"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        help="Status of the offer"
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property ID", required=True)
    validity = fields.Integer(default=7, string='Validity')
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "Offer price must be positive",
        ),
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
        return True

    def refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.buyer = False
            record.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property_id = record['property_id']
            property = self.env['estate.property'].browse(property_id)
            if property and property.best_price:
                if record['price'] <= property.best_price:
                    raise UserError('Offer price must be greater than best offer price')
            if property.state == 'new':
                property.state = 'received'
        return super().create(vals)
