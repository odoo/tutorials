import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    set_salesperson(salesperson){
        console.log("set_salesperson");
        if(salesperson){
            this.update({salesperson_id : salesperson})
        }
    },
});
