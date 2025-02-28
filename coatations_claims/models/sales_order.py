from odoo import api,fields,models

class SaleOrder(models.Model):
    _inherit= "sale.order"

    coation_ids = fields.Many2many("coatations.claims")

    @api.onchange("partner_id")
    def _onchange_is_reseller(self):
        print("------------------------------------------------------------------------------------------------------------------------------------------")
        coatation_records = self.env["coatations.claims"].search([('client_id','=',self.partner_id.name)])
        if coatation_records:
                print("")
                print(type(self.env["coatations.claims"].search([('client_id','=',self.partner_id.name)])))
                print()
                print("IT IS A RESELLER!!!")
                print("")
                print("")
                #fetching all the coatations based on customer name
                for coatation in coatation_records:
                    print(coatation.name)
                    print(coatation.coation_lines_ids.product_id)
                   
                pass #apply some function to add coation value.

