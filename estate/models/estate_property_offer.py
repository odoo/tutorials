from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    name = fields.Char(string="Property Offer", required=True)
    price = fields.Integer(string="Price", required=True)
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    # Connected with estate_Property
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        readonly=False,
    )

    # It gets changed on each changes because it works based on cache
    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for records in self:
            default_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            records.date_deadline = fields.Date.add(default_date, days=records.validity)

    # Inverse is triggered when the computed field is written (usually during save),not during live editing.
    def _inverse_deadline(self):
        for records in self:
            default_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            if records.date_deadline:
                records.validity = (records.date_deadline - default_date).days

    def save_offer(self):
        for record in self:
            if record.status != "accepted" or record.status != "refused":
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "accepted"

    def cancel_offer(self):
        for record in self:
            if record.status != "accepted" or record.status != "refused":
                record.status = "refused"
                if record.property_id.buyer_id == record.partner_id:
                    record.property_id.selling_price = False
                    record.property_id.state = False

    # Inserted price must be positive - SQL constraint
    _check_price = models.Constraint(
        "CHECK(price >= 0)", "Price filled must be positive"
    )
