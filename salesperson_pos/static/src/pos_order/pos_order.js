import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
patch(PosOrder.prototype, {
  set_salesperson(salespersonID) {
    try {
      this.update({ salesperson_id: salespersonID });
    } catch (error) {
      console.log("error", error);
    }
  },
});
