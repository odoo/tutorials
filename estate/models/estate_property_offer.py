from odoo import fields, models, api, exceptions

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "offer for an estate"
    _sql_constraints = [
        ('check_price', 'CHECK(price>0)', 
         'The offer price is stricly positive'),
    ]
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')],
        copy=False, string="Status")
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', required=True, string="Property")
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline Date")
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type")

    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        estate_property = self.env['estate.property'].browse(vals_list[0]['property_id'])

        if estate_property.best_price > vals_list[0]['price']:
            raise exceptions.UserError('Existing offer have higher offred price')

        estate_property.state = 'offer received'

        return super().create(vals_list)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date).days

    # ----------- Action Fun
    def action_set_accepted(self):
        for record in self:
            if record.property_id.state == 'offer accepted':
                raise exceptions.UserError("Accept only one offer")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer accepted'
        return True

    def action_set_refused(self):
        for record in self:
            record.status = 'refused'
        return True
