from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = ""
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    estate_property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self) -> None:
        record: EstatePropertyOffer
        for record in self:
            create_date: fields.Datetime = record.create_date or fields.Datetime.now()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self) -> None:
        # FIXME wasted too much time on this.
        record: EstatePropertyOffer
        for record in self:
            pass

    @api.model_create_multi
    def create(self: 'EstatePropertyOffer', vals_list: list[api.ValuesType]):
        for val in vals_list:
            property_id: int = val['estate_property_id']
            property = self.env['estate.property'].browse(property_id)
            prices = property.estate_property_offer_ids.mapped('price')
            min_price = min(prices or [0])
            if val['price'] < min_price:
                raise exceptions.UserError(f'Price cannot be lower than ${min_price}')


        return super().create(vals_list)

    def action_accept_offer(self) -> bool:
        record: EstatePropertyOffer
        for record in self:
            all_offers = record.estate_property_id.estate_property_offer_ids
            if all_offers.filtered(lambda o: o.status == "accepted"):
                raise exceptions.UserError("You can't accept two offers")
            record.estate_property_id.buyer_id = record.partner_id
            record.estate_property_id.selling_price = record.price
            record.estate_property_id.state = "offer_accepted"
            record.status = "accepted"
        return True

    def action_refuse_offer(self) -> bool:
        record: EstatePropertyOffer
        for record in self:
            record.status = "refused"
        return True

    _sql_constraints: list[tuple[str, str, str]] = [
        (
            "offer_price_strictly_positive",
            "CHECK(offer > 0)",
            "Offer price must be stricly positive.",
        ),
    ]

    property_type_id = fields.Many2one(related="estate_property_id.property_type_id", store=True)
