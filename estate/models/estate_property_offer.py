from odoo import api, models, fields
from datetime import timedelta
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class EstatePropertyOffer (models.Model): 
    _name = "estate.property.offer"
    _description = "Lời đề nghị"
    
    price  = fields.Integer( string="Price")
    validity  = fields.Integer( string="Validity (days)", default=7 )
    date_deadline  = fields.Date( string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline", store=True)
    state = fields.Selection(selection=[("accepted", "Accepted"),
            ("refused", "Refused")], string="Status" , default=False)
    partner_id  = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    _order = "price desc"
    property_type_id = fields.Many2one("estate.property.type",related="property_id.property_type_id", string="Property Type", store=True)
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
         if record.create_date:
          base_date = record.create_date.date()
         else :
          base_date = fields.Date.today()
         record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
         if record.create_date:
          base_date = record.create_date.date()
         else :
          base_date = fields.Date.today()
         diff = record.date_deadline - base_date
         record.validity = max(0, diff.days)
    def action_confirm(self):
        for record in self:
            print(f"--- Đang xác nhận Offer cho nhà: {record.property_id.name} ---")
            record.state = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            
        return True

    def action_refuse(self):
        for record in self:
            record.state = 'refused'
        return True
    
    def unlink(self):
        for record in self:
            if record.state in ['accepted', 'refused']:
                raise UserError("Không thể xóa lời đề nghị đã được chấp nhận hoặc bị từ chối!")
        return super(EstatePropertyOffer, self).unlink()
    
    @api.model
    def create(self, vals):
      property_record = self.env['estate.property'].browse(vals.get('property_id'))
      max_price = max(property_record.offer_ids.mapped('price'), default=0)
      if vals.get('price', 0) < max_price:
        raise UserError(f"Giá phải cao hơn {max_price}!")
      property_record.state = 'offer_received'
      return super().create(vals)
    
    _sql_constraints=[
       ('check_price', 'CHECK(price > 0)','Giá đề nghị phải > 0')
    ]

 

