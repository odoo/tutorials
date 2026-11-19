from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Define offers for properties"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start, days=record.validity) #if validity is not set, it is treated as 0

    def _inverse_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start).days

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.state = "offer_received"
        return offers

    def action_accept(self):
        for record in self:
            match record.property_id.state:
                case "offer_accepted":
                    raise UserError("An offer has already been accepted for this property.")
                case "sold":
                    raise UserError("The property has already been sold")
                case "cancelled":
                    raise UserError("This property has been cancelled")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price should be strictly positive',
    )
