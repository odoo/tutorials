from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = ['estate.property']
    
    def sold(self):

        print(" reached ".center(100, '='))
        self.check_access('write') 
        account_move = self.env['account.move'].sudo().create({
            "move_type" : "out_invoice",
            "partner_id" : self.buyer_id.id,
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
