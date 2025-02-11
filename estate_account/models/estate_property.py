from odoo import models, fields, api, Command



class EstateProperty(models.Model):
    _inherit = ['estate.property']
    
    def sold(self):
        account_move = self.env['account.move'].create({
            "name" : self.name,
            "move_type" : "out_invoice",
            "partner_id" : self.buyer_id.id,
            "journal_id" : self.env['account.journal'].search([('type','=','sale')],limit=1),
            "line_ids": [
                Command.create({
                    "name": self.name,
                    "price_unit":self.selling_price,
                }),
                Command.create({
                    "name": f"{self.name}- 6% of selling price",
                    "price_unit":self.selling_price * 0.06,
                }),
                Command.create({
                    "name": f"{self.name} - Administrative fees",
                    "price_unit":100,
                })
            ]
        })
        print("INvoice Created!!!!!!!!!!!!!!!!!!!!1")
        print("INvoice Created!!!!!!!!!!!!!!!!!!!!1")
        print("INvoice Created!!!!!!!!!!!!!!!!!!!!1")
        print("INvoice Created!!!!!!!!!!!!!!!!!!!!1")
        print("INvoice Created!!!!!!!!!!!!!!!!!!!!1")
        print("INvoice Created!!!!!!!!!!!!!!!!!!!!1")
        print("INvoice Created!!!!!!!!!!!!!!!!!!!!1")
        return super().sold()
 