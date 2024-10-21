from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    price = fields.Float("Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
        string="Status"
        )
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_id = fields.Many2one("estate.property", string="Property")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer("Validity (in days)", default="7")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date)
            base_date = create_date if create_date is not None else fields.Date.today()
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def accept_offer(self):
        for record in self:
            query = """
            SELECT
                count(*) as offer_accepted
            FROM
                estate_property_offer
            WHERE
                property_id = %(property_id)s
            AND
                status = 'accepted'
            AND
                id != %(id)s
            """
            self.env.cr.execute(query, {
                'property_id': record.property_id.id,
                'id': record.id
            })

            query_result = self.env.cr.dictfetchone()

            if query_result['offer_accepted'] > 0:
                raise UserError('Only one offer can be accepted per property.')
            if not record.partner_id:
                raise UserError('An offer must be linked to a client !')
            else:
                record.status = "accepted"
                record.property_id.state = "offer_accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.buyer_id = None
                record.property_id.selling_price = "0"
            record.status = "refused"
        return True

    _sql_constraints = [
        (
            'check_offer_price',
            'CHECK(price > 0)',
            'The offer price of a propery should always be positive'
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):

        new_offers = []

        for vals in vals_list:

            linked_property = self.env['estate.property'].browse(vals["property_id"])

            if vals["price"] < max(linked_property.offer_ids.mapped('price'), default=0):
                raise UserError("The offer price is smaller than a previous offer, this is not authorized")

            if linked_property.state == "new":
                linked_property.state = "offer_received"

            new_offers.append(super().create(vals))

        return new_offers
