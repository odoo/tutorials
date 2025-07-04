from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers of Estate property "

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection = [
            ('accepted','Accepted'),
            ('refused','Refused')
        ], copy=False,string='Status'
    )

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    partner_id = fields.Many2one("res.partner", string="Partner",copy=False,required=True)
    property_id = fields.Many2one("estate.property",copy=False,required=True)



    @api.depends('create_date','validity')
    def _compute_deadline_date(self):
        for offer in self:
            create_dt = offer.create_date or fields.Date.today()
            offer.date_deadline = create_dt + relativedelta(days=offer.validity)


    def _inverse_deadline_date(self):
        for offer in self:
            if offer.date_deadline:
                create_dt = (offer.create_date or fields.Datetime.now()).date()
                delta = (offer.date_deadline - create_dt).days
                offer.validity = delta
            else:
                offer.validity = 0
