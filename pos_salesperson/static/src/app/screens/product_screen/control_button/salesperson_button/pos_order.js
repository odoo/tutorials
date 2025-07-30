import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    setSalesPerson(salesperson, currentOrder) {
        this.update({ salesperson_id: salesperson })
        console.log(currentOrder)
    },
})
