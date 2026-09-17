from odoo import models, fields, api
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_id_state = fields.Selection(related="property_id.state")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must be strictly positive",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = (
                fields.Date.to_date(record.create_date)
                if record.create_date
                else fields.Date.today()
            )
            record.validity = (record.date_deadline - base_date).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            property_id.state = 'offer_received'
            for record in property_id.offer_ids:
                if record.price > vals['price']:
                    raise UserError("Cannot create an offer with a lower value than an existing one")
        return super().create(vals_list)

    def action_accept(self):
        # TODO Investigate using write() to update records
        for record in self:
            if record.property_id.state in ("offer_accepted", "sold", "cancelled"):
                err_msg = f"Cannot accept offer on property that is {record.property_id.state}"
                raise UserError(err_msg)
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
