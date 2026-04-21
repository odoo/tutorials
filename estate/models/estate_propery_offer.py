from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", required=True)
    property_type_id = fields.Many2one("estate.property.type")
    deadline = fields.Date(
        string="Deadline",
        default=datetime.today(),
        compute="_compute_validity_days",
        inverse="_inverse_deadline",
        store=True
    )
    validity_days = fields.Integer(default=7)

    _check_expected_price = models.Constraint(
        'CHECK(price > 0)',
        'The price must be strictly positive',
    )

    @api.depends("validity_days")
    def _compute_validity_days(self):
        for record in self:
            if record.deadline and record.validity_days > 0:
                record.deadline = record.deadline + timedelta(
                    days=record.validity_days)
            else:
                record.deadline = fields.Date.today()

    @api.depends("deadline")
    def _inverse_deadline(self):
        for record in self:
            if record.deadline:
                diff = record.deadline - fields.Date.today()
                record.validity_days = diff.days

    def accept_offer(self):
        for record in self:
            if record.status == "accepted":
                raise ValidationError("the offer already accepted")

            if record.property_id.garden_orientation == "south" and record.property_id.expected_price > record.price:
                raise ValidationError("The south-facing garden can only be accepted if above expected price")

            if record.property_id.selling_price == 0:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id
                record.property_id.state = "offer accepted"

    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                raise ValidationError(
                    "You're not eligible to refused an accepted offer"
                )
            record.status = "refused"

    @api.model
    def create(self, val_list):
        for vals in val_list:
            property_id = vals.get('property_id')

            existing_offers = self.search([
                ('property_id', '=', property_id)],
                order='price desc', limit=1)

            if existing_offers and vals.get('price', 0) < existing_offers.price:
                raise UserError(f"You cannot create an offer lower than {existing_offers.price}.")

            property_record = self.env['estate.property'].browse(property_id)
            property_record.state = 'offer received'

        return super().create(val_list)
