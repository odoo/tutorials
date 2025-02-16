from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer list for estate properties"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        readonly=True,
        help="Status of the offer",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default="7")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + relativedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 7

    def action_confirm(self):
        for record in self:
            if record.status == "accepted":
                raise ValidationError("Already accepted.")
            else:
                record.status = "accepted"
                record.property_id.partner_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = "offer_accepted"
                other_offers = record.property_id.offer_ids - record
                other_offers.write({"status": "refused"})
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "refused":
                raise ValidationError("Already refused.")
            else:
                record.status = "refused"
        return True

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Price must be positive."),
    ]
    @api.model_create_multi
    def create(self, vals_list):
        # Iterate through each record's values in the batch
        for vals in vals_list:
            property_id = vals["property_id"]
            property_record = self.env["estate.property"].browse(property_id)

            # Validate the price for each record
            if property_record.expected_price > vals["price"] or vals["price"] < property_record.best_price:
                raise UserError("Price is too low!")

            # Update property state for each related property
            property_record.state = "offer_received"

        # Call the super method to create records in batch
        return super().create(vals_list)
