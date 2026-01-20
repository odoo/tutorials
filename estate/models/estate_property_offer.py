from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "ESTATE Property Offer"
    _order = "price desc"

    description = fields.Text(string="Description")
    price = fields.Float('Price')
    validity = fields.Float('Validity (Days)', default=7.0)
    date_deadline = fields.Date('Deadline',
                                compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline")  # Computed Field

    offer_status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        help="Choose the state of the offer",
        copy=False,
    )
    property_id = fields.Many2one("estate.property", string="Property", required=True)  # Foreign_Key (Property)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)  # Foreign_Key (Partner Contact)
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)  # Related_Field (Property Type)

    # date_deadline is computedFailed, so it called when its Dependencies changes
    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer_record in self:
            creation_date = offer_record.create_date.date() if offer_record.create_date else fields.Date.today()  # offer_record.create_date is a default field & use creation_date to handle crashing at time of creation.
            offer_record.date_deadline = creation_date + timedelta(days=offer_record.validity)

    # date_deadline is computedFailed but not readOnly, so it called when date_deadline changes manually
    def _inverse_date_deadline(self):
        for offer_record in self:
            creation_date = offer_record.create_date.date() if offer_record.create_date else fields.Date.today()  # offer_record.create_date is a default field & use creation_date to handle crashing at time of creation.
            valid = offer_record.date_deadline - creation_date
            if offer_record.date_deadline:
                offer_record.validity = valid.days

    # SQL constraints
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'An offer price must be strictly positive',
    )

    # CRUD Method (on_create New Offer)
    @api.model
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val.get("property_id"))

            if property.estate_state == "new":
                property.estate_state = "offer_received"

            if "price" in val and property.offer_ids:
                if val["price"] < max(property.offer_ids.mapped("price")):
                    raise ValidationError("You cannot create an offer with a lower amount than the existing highest offer")
        return super().create(vals)

    def action_accept(self):
        for offer_record in self:
            property = offer_record.property_id
            if property.estate_state in ['sold', 'cancelled']:
                raise UserError(f"You cannot accept an offer on '{property.estate_state}' property !")

            accepted_offers = property.offer_ids.filtered(lambda o: o.offer_status == 'accepted')
            if accepted_offers and offer_record not in accepted_offers:
                raise UserError("Only one offer can be accepted at a time for a property")

            if float_compare(offer_record.price, property.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError("The selling price must be at least 90% of the expected price, You must reduce the expected price if you want to accept this offer")

            offer_record.offer_status = 'accepted'
            property.estate_state = 'offer_accepted'
            property.partner_id = offer_record.partner_id
            property.selling_price = offer_record.price
        return True  # to avoid warning in logs as it's a public method

    def action_refuse(self):
        for offer_record in self:
            property = offer_record.property_id
            if property.offer_ids.filtered(lambda o: o.offer_status == 'accepted') == offer_record:  # if the refused offer is the accepted one
                property.estate_state = 'new'
                property.selling_price = 0.0
            offer_record.offer_status = 'refused'
        return True  # to avoid warning in logs as it's a public method
