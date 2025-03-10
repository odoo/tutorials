from datetime import datetime

from odoo import fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    select_shipping_date =  fields.Datetime(default=fields.Datetime.now)

    def _process_saved_order(self, draft):
        if draft and  self.select_shipping_date:
            self._create_order_picking()
            self._compute_total_cost_in_real_time()
        return super(PosOrder, self)._process_saved_order(draft)
