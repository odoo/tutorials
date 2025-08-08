/** @odoo-module **/

import { Component, useRef } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SecondUomDialog extends Component {
    static template = "pos_second_uom.SecondUomDialog";
    static props = {
        close: { type: Function },
        product: { type: Object },
        secondUomName: {type: String, optional: true},
    };
    static components = { Dialog }; 
    setup() {
       this.pos= usePos();
       this.inp_qty = useRef("inp")
       this.ratio = this.computeRatio(this.props.product)
    }
    computeRatio(product) {
        if (product.uom_id && product.pos_second_uom_id) {
            return product.uom_id.factor / product.pos_second_uom_id.factor;
        }
        return 1;
    }
    confirm() {
        const qty = parseFloat(this.inp_qty.el.value)
        const orderLine = this.pos.get_order().get_selected_orderline();
        
        if (orderLine) {
            orderLine.set_quantity(qty * this.ratio);
        }
        this.props.close(); 
    }
}
