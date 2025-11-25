from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one(
        "estate.property", required=True, string="Property", ondelete="cascade"
    )
    validity = fields.Integer(default=7)
    deadline_date = fields.Date(
        compute="_compute_deadline_date", inverse="_inverse_deadline_date"
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _postive_price = models.Constraint(
        "CHECK (price > 0)",
        "The expected price must be strictly positive"
    )

    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.deadline_date = fields.Date.add(create_date, days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (record.deadline_date - create_date.date()).days

    def button_accept_offer(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise exceptions.UserError(
                    f"Property '{offer.property_id.name}' is already sold"
                )
            offer.property_id.write({
                    "buyer_id": offer.partner_id,
                    "selling_price": offer.price,
                    "state": "offer_accepted"
                })
            offer.status = "accepted"
        return True

    def button_refuse_offer(self):
        for offer in self:
            if offer.property_id.state == "sold" and offer.status == "accepted":
                raise exceptions.UserError(
                    f"Property '{offer.property_id.name}' is already sold to '{offer.partner_id.name}'"
                )
            offer.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            property_id = self.env['estate.property'].browse(val['property_id'])
            if property_id.offer_ids and max(offer.price for offer in property_id.offer_ids) > val['price']:
                raise exceptions.UserError("An offer with a higher price exists")
            property_id.state = "offer_received"
        return super().create(vals_list)
