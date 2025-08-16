import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
  get_salesperson() {
    return this.salesperson_id;
  },
  set_salesperson(salesperson) {
    this.salesperson_id = salesperson;
  },
});
