from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    _sql_constraints = (
        ('positive_price', 'CHECK(price > 0)',
         'Offer price should be positive'),
    )

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")],
        copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_deadline")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date().today()
            record.date_deadline = fields.Date.add(
                create_date,
                days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date().today()
            record.validity = (record.date_deadline -
                               create_date.date()).days

    def accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    offer.status = 'refused'

            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

        return True

    def refuse(self):
        for record in self:
            record.status = 'refused'

        return True

    @api.model_create_multi
    def create(self, vals):
        property = self.env["estate.property"].browse(vals['property_id'])
        for offer in property.offer_ids:
            if float_compare(vals['price'], offer.price, precision_digits=3) < 0:
                raise UserError(
                    "Cannot add an offer with value lower than existing offers")

        property.state = 'received'
        return super().create(vals)
