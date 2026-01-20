from odoo import models, fields, api
from odoo.exceptions import ValidationError 

class SaleOrder(models.Model): 
    _inherit = "sale.order"

    original_promise_date = fields.Date()
    revised_promise_date = fields.Date(tracking=True)
    promise_date_history_ids = fields.One2many('promise.date.record', 'sale_order_id', string="Promise Date History")
    
    @api.onchange('original_promise_date')
    def _onchange_original_promise_date(self):
        """Changes the commitment(delivery) date on changes of original promise date when order is in quatation state"""
        self.commitment_date = self.original_promise_date
    
    def action_confirm(self):
        for order in self:
            """Raise error if original promise date is not set"""
            if not order.original_promise_date:
                raise ValidationError("You cannot confirm this quotation without setting the Original Promise Date.")
            
            """Stores the first change in revised promise date None to set date"""
            self.env['promise.date.record'].create({
                'sale_order_id': order.id,
                'changed_by': self.env.user.id,
                'from_date': None,
                'to_date': order.original_promise_date,
            })

            """Changes the commitment(delivery) date when first time original promise date is set"""
            order.commitment_date = order.original_promise_date
            message = f"Revised Promise Date changed from {None} to {order.original_promise_date} by {self.env.user.name}"
            order.message_post(body=message)

        return super(SaleOrder, self).action_confirm()

    def write(self,vals):
        for record in self : 
            """Raise error on changing the original promise date after the confirmation of sale order"""
            if 'original_promise_date' in vals and record.state == 'sale':
                raise ValidationError("You cannot modify the Original Promise Date once the order is confirmed.")

            """Store the value of revised promise date before saving the record to the database"""
            old_date = record.revised_promise_date

        result = super(SaleOrder,self).write(vals)

        """Store the new revised promise date and save that record to the promise.date.record model"""
        for record in self: 
            new_date = record.revised_promise_date
            if old_date != new_date :
                record.commitment_date = new_date
                if record.id : 
                    self.env['promise.date.record'].create({
                        'sale_order_id':record.id,
                        'changed_by':self.env.user.id,
                        'from_date':old_date,
                        'to_date':new_date,
                    })
                message = f"Revised Promise Date changed from {old_date or 'Empty'} to {new_date} by {self.env.user.name}"
                record.message_post(body=message)
        
        return result 

    def create(self, vals):
        """Raise error on not setting original promise date"""
        if  not vals.get('original_promise_date') : 
            raise ValidationError("Set the Original Promise Date")

        """ Raise error on the set of original promise date lower than the order date"""
        date_order_value = fields.Date.to_date(vals.get('date_order')) if vals.get('date_order') else None
        original_promise_date_value = fields.Date.to_date(vals.get('original_promise_date')) if vals.get('original_promise_date') else None

        if date_order_value and original_promise_date_value and date_order_value > original_promise_date_value:
            raise ValidationError("The Original Promise date must be greater than the order date")
        
        """Set the revised promise date on the first creation of the sale order"""
        if not vals.get('revised_promise_date') and vals.get('original_promise_date'):
            vals['revised_promise_date'] = vals['original_promise_date']

        return super(SaleOrder, self).create(vals)
    