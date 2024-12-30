from odoo import models, fields, api
from datetime import timedelta, datetime


class ProductWarrantyWizard(models.TransientModel):
    _name = "product.warranty.wizard"
    _description = "wizard to add multiple offers"

    product_ids = fields.One2many('product.warranty.list', "product_ids", string="warranty Lines") 
   
    def add_warranty(self):
        for record in self.product_ids:
            self.env['sale.order.line'].create({
                'product_id': record.year.product_id.id,
                'product_uom_qty': 1,
                'order_id': self._context.get('active_id'),
                'price_unit': record.product_id.list_price * record.year.percentage / 100,
                'warranty_line_id' :record.main_order_line.id,
                'name': "Extended Warranty for " + str(record.main_order_line.name) + " End Date: " + str(record.end_date or "N/A")


            })
             

class ProductWarrantyList(models.TransientModel):
    _name= "product.warranty.list"
    _description="add warranty list"

    product_ids= fields.Many2one("product.warranty.wizard", string="warranty Lines") 
    product_id = fields.Many2one('product.product',string="Product",required=True)
    year= fields.Many2one("warranty.configuration",string="Warranty Years",required= True, default=lambda self: self.env['warranty.configuration'].search([], limit=1))
    end_date= fields.Date(string="End Date", compute="_compute_end_date",store=True)
    warranty_line_id = fields.Many2one('sale.order.line' , string=" Warranty Line")
    main_order_line = fields.Many2one('sale.order.line', string="Order Line")

    @api.depends('year')
    def _compute_end_date(self):
        for record in self:
            if record.year:
                record.end_date= datetime.now() + timedelta(days=record.year.year*365)