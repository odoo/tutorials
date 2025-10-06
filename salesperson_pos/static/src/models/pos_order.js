/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {PosOrder} from "@point_of_sale/app/models/pos_order";

patch(PosOrder.prototype, {
    setSalesperson(sales_person){
        this.update({salesperson: sales_person});
    },
    getSalesperson(){
        return this.salesperson;
    }
})