from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a real estate property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True, help="The client who made this offer")
    property_id = fields.Many2one('estate.property', required=True, help="The property for which the current offer is being made")
    validity = fields.Integer(default=7, string="Offer Validity (Days)", help="How many days is this offer valid for?")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK (price > 0)', 'Price must be strictly positive!')
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        tmp_date = fields.Date.today()
        for offer in self:
            offer.date_deadline = fields.Date.add(offer.create_date or tmp_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = fields.Date.from_string(offer.create_date or fields.Date.today())
            end_date = fields.Date.from_string(offer.date_deadline)
            difference = (end_date - start_date).days
            offer.validity = difference

    def action_accept(self):
        for record in self:
            record.property_id.offer_ids.action_refuse()
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_acepted'

    def action_refuse(self):
        self.status = "refused"

    @api.model
    def create(self, vals):
        prop = self.env['estate.property'].browse(vals['property_id'])
        if float_compare(vals['price'], max(prop.offer_ids.mapped('price'), default=0), precision_digits=2) < 0:
            raise UserError(_("Price must be higher than highest bid!"))
        prop.state = 'offer_received'
        return super().create(vals)
