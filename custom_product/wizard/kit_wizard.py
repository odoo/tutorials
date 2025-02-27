from odoo import fields,models,api

class KitWizard(models.TransientModel):
    _name="kit.wizard"
    _description="Kit Wizard"

    product_id = fields.Many2one('product.product',string="Kit Product",required=True)  # refers to main product , (its product.product)
    component_ids = fields.One2many("kit.wizard.line", "wizard_id", string="Sub Products") 
    # one product has many sub products so one2many, this componet refer/contains sub-products for perticular parent product.

    @api.model
    def default_get(self,fields):
        res = super().default_get(fields)
        context = self.env.context

        sale_order_line_id = context.get("active_id") # gives you just int. id of order line from which wizard btn is selected

        if not sale_order_line_id:
            return res
        
        sale_order_line = self.env['sale.order.line'].browse(sale_order_line_id)  # gives you record-set releted to that order line. 

        """
        ex. sale_order_line_id gives you record id=25,
        at 25 lets say you have record
        product_id:10,
        name:lapto,
        ...
        you browse gives you that.
        """

        if sale_order_line.product_id.product_tmpl_id.is_kit:
            components = []
            for kit_product in sale_order_line.product_id.product_tmpl_id.kit_product_ids:
                """
                # here product_id will give you id of product.product , and for accesing the sub product you need many2many field named kit_product_ids determine
                in product.template , so for that we'll access the product_tmpl_id and from that we will go thorugh all sub products.
                """
                components.append((0,0 ,{
                    "product_id" : kit_product.id,  #product.product id->subproduct_id
                    "quantity" : 1.0,
                    "price" : kit_product.lst_price,
                }))
            
            res.update({
                "product_id":sale_order_line.product_id.id,  # initilize the main product with which button is selected and wizard is opened (in ex.Floor painitng)
                "component_ids":components              # determine order lines of wizard
            })
        return res

    def action_confirm(self):   
        print("Kit Wizard Confimed")


class KitWizardLine(models.TransientModel):
    _name="kit.wizard.line"
    _description = "Kit Wizard Line"

    wizard_id = fields.Many2one("kit.wizard",string="Wizard",required=True,ondelete="cascade")

    #-------------component_ids fields--------------------------------------------------------
    product_id = fields.Many2one("product.product",string = "Component" ) 
    quantity = fields.Float(string="Quantity",default=1.0)
    price = fields.Float(string="Price")