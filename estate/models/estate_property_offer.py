from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string='Status',
        selection=[('received', 'Received'), ('accepted', 'Accepted'), ('refused', 'Refused')],
        copy="False",
        default='received',
        help="Status of the Offer")
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        help='Person making the offer'
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property ID',
        required=True
    )
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_deadline',
        inverse='_inverse_deadline'
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type")

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = ((record.create_date) + relativedelta(days=record.validity)).date()
            elif record.validity:
                record.date_deadline = (fields.Datetime.now() + relativedelta(days=record.validity)).date()
            else:
                record.date_deadline = False

    @api.depends("create_date", "date_deadline")
    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 0

    def action_accept_button(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = 'offer accepted'

    def action_refuse_button(self):
        self.status = 'refused'
        self.property_id.buyer_id = ''

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
        'The offer price should be more than 0 and striclty positive')
    ]

    @api.model
    def create(self, vals):
        offer = vals.get('property_id')
        self.property_id.browse(offer).state = 'offer received'
        search_price = vals.get('price')
        record = self.search([('property_id', '=', offer)])
        if record:
            best = max(record.mapped('price'))
            if search_price < best:
                raise UserError("New offer price cannot be less than previous offers")
        return super().create(vals)
