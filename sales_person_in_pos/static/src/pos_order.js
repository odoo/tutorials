import { patch } from "@web/core/utils/patch";
import { PosOrder } from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {

    setSalesperson(salesperson) {
        this.update({ salesperson_id: salesperson });
    },

    getSalesperson() {
        return this.salesperson_id;
    }

});
