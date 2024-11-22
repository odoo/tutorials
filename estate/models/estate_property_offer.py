from datetime import timedelta

from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = ''
    _order = "price desc"
    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
        'The price of an offer MUST be postive.'),
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ],
        copy=False,
    )
    validity = fields.Integer(string="Validity (Days)", default=7)

    # Relations
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    # computed
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    # region Compute methodes
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    # endregion

    # region CRUD
    @api.model
    def create(self, vals_list):
        self.env['estate.property'].browse(vals_list['property_id']).action_set_offer_received()
        return super().create(vals_list)

    # endregion

    # region actions
    def action_set_accepted(self):
        for record in self:
            record.property_id.action_set_offer_accepted(self)
            record.status = 'accepted'

    def action_set_refused(self):
        for record in self:
            record.status = 'refused'

    # endregion
