from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class list_warranty(models.TransientModel):
    _name = "product.list.warranty"
    _description = "product.warranty.configuration"

    product_id = fields.Many2one(
        "product.product",
        string="product",
        required=True,
        domain=[("is_warranty", "=", "True")],
    )
    qty = fields.Integer(default=1)
    order_line_id = fields.Integer(required=True)
    warranty_id = fields.Many2one(
        "product.warranty.configuration", string="product warranty"
    )
    enddate = fields.Char(string="enddate", readonly=True)

    add_warranty_id = fields.Many2one("product.add.warranty", string="add_warranty")

    @api.onchange("warranty_id")
    def _onchange_enddate(self):
        for record in self:
            if record.warranty_id:
                record.enddate = str(
                    (
                        datetime.today() + relativedelta(years=record.warranty_id.years)
                    ).date()
                )
            else:
                record.enddate = ""


