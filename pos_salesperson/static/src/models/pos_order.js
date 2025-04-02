import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    setSalesperson(salesperson) {
        if (salesperson) {
            this.salesperson_id = salesperson.id;
            this.salesperson_name = salesperson.name;
        } else {
            this.salesperson_id = null;
            this.salesperson_name = null;
        }
    },

    getSalesperson() {
        return this.salesperson_id ? { id: this.salesperson_id, name: this.salesperson_name } : null;
    },
});
