from odoo import models, fields, api

class ProductKit(models.TransientModel):
    _name="product.kit"
    
    product_kit_line_ids= fields.One2many(comodel_name='product.kit.lines', inverse_name="product_kit_id")
    
    @api.model
    def default_get(self, fields_list):
        product_template= self.env['product.template'].browse(self.env.context.get('product_template_id')) 
        sale_order_line_id = self.env['sale.order.line'].browse(self.env.context.get('sale_order_line_id'))
        
        defaults = super().default_get(fields_list)
        product_kit_line_ids=[]
        
        is_kit_line_exits={}
        
        #Handling subproduct added later case in future case for that Taking union of existing and not existing line()
        for c_pro in sale_order_line_id.linked_product_kit_ids:
            product_kit_line_ids.append({
                'product_id':c_pro.product_id.id,
                'quantity': c_pro.product_uom_qty,
                'price': c_pro.prev_filled_unit_price
            })
            is_kit_line_exits[c_pro.product_id.id]=True
        for c_pro in product_template.sub_products_ids:
            if(not is_kit_line_exits.get(c_pro.id, False)):
                product_kit_line_ids.append({
                    'product_id': c_pro.id,
                    'quantity': 1,
                    'price': 0
                })
            
        line= self.env['product.kit.lines'].create(product_kit_line_ids)
        product_kit_line_ids= line
            
        defaults['product_kit_line_ids']=product_kit_line_ids
        return defaults

    #adding Sale kit product into sale order line
    def action_add_kit_values_to_product(self):
        sale_order_line= self.env['sale.order.line'].search([('id','=',self.env.context.get('active_id'))])
        template_sub_products=self.product_kit_line_ids
        
        sub_product_total= 0
        
        #is no sale.order.line exist related to the current product order line only then create else update
        if(len(sale_order_line.linked_product_kit_ids)==0):    
            for prod in template_sub_products:
                self.env['sale.order.line'].create({
                    'linked_product_kit_id': sale_order_line.id,
                    'order_id': sale_order_line.order_id.id,
                    'product_id': prod.product_id.id,
                    'product_uom_qty': prod.quantity,
                    'price_unit': 0,
                    'customer_lead':0,
                    'prev_filled_unit_price': prod.price
                })
                sub_product_total+= prod.quantity * prod.price

            sale_order_line.update({
                'price_subtotal': sale_order_line.price_subtotal+sub_product_total
            })    
        else:
            new_subtotal= sale_order_line.price_subtotal
            #remove the old price and add new price;
            # formula==> new_subtotal = new_subtotal - (old_qty*price_pu) + (new_qty*price_pu)
            # to update the linked_kit_lines details for next time
            
            old_price=0
            for old_line in sale_order_line.linked_product_kit_ids:
                old_price+= old_line.product_uom_qty * old_line.prev_filled_unit_price
            
            incomming_price=0
            for new_line in template_sub_products:
                incomming_price+= new_line.quantity * new_line.price
            
            new_subtotal= new_subtotal - old_price + incomming_price
            
            for old_line in sale_order_line.linked_product_kit_ids:
                for new_line in template_sub_products:
                    if(old_line.product_id.id == new_line.product_id.id):
                        old_line.update({
                            'prev_filled_unit_price': new_line.price,
                            'product_uom_qty': new_line.quantity,
                            'price_unit':0
                        })
    
            sale_order_line.update({
                'price_subtotal': new_subtotal
            })
            
        template_sub_products.unlink()
        return True

class ProductKitLines(models.TransientModel):
    _name="product.kit.lines"
    
    product_kit_id= fields.Many2one(comodel_name="product.kit")
    product_id= fields.Many2one(string="product", comodel_name='product.product')
    quantity= fields.Float(string="quantity")
    price= fields.Float(string="price")
