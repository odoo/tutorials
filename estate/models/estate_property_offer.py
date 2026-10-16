from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    state = fields.Selection(string="Status", copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    property_id = fields.Many2one("estate.property", string="Property")
    partner_id = fields.Many2one("res.partner", string="Partner")
    validity = fields.Integer("Validity")
    date_deadline = fields.Date("Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price of an offer should be strictly positive.',
    )

    # ------------------------------------------------------------
    # COMPUTED FIELDS
    # ------------------------------------------------------------

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date if record.create_date else fields.Datetime.now()
            record.date_deadline = fields.Date.add(date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    # ------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals["property_id"]
            prop = self.env["estate.property"].browse(property_id)
            if prop.offer_ids and vals["price"] < min(prop.offer_ids.mapped("price")):
                raise ValidationError(_("You cannot create a new offer with a lower price than existing offer!"))
            prop.state = "received"
        return super().create(vals_list)

    # ------------------------------------------------------------
    # ACTION METHODS
    # ------------------------------------------------------------

    def action_accept(self):
        self.ensure_one()
        self.state = "accepted"
        prop = self.property_id
        prop.buyer = self.partner_id
        prop.selling_price = self.price
        prop.state = "accepted"
        for offer in prop.offer_ids:
            if self.state == "accepted" and offer.id != self.id:
                offer.state = "refused"

    def action_refuse(self):
        self.ensure_one()
        self.state = "refused"
