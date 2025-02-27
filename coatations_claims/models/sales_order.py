from odoo import api,fields,models

class SaleOrder(models.Model):
    _inherit= "sale.order"

    coation_ids = fields.Many2many("coatations.claims")

    @api.onchange("partner_id")
    def _onchange_is_reseller(self):
        print("------------------------------------------------------------------------------------------------------------------------------------------")
        if self.env["coatations.claims"].search([('client_id','=',self.partner_id.name)]):
                print("")
                print("")
                print("")
                print("IT IS A RESELLER!!!")
                print("")
                print("")
                pass #apply some function to add coation value.

