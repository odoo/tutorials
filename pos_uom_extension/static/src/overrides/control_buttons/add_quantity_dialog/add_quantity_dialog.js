import { Dialog } from "@web/core/dialog/dialog";
import { Component, useRef } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class AddQuantityDialog extends Component {
    static template = "pos_uom_extension.AddQuantityDialog";
    static components = { Dialog };
    static props = {
        close: { type: Function },
        product: { type: Object },
        secondUomName: {type: String, optional: true},
    };

    setup(){
        this.pos = usePos();
        this.input_qty = useRef("quantityInput");
        this.uom_ratio = this.computeUomRatio(this.props.product)
    }

    computeUomRatio(product) {
        if (product.uom_id && product.second_uom_id) {
            return product.uom_id.factor / product.second_uom_id.factor;
        }
        return 1;
    }
    
    confirm() {
        const quantity = parseFloat(this.input_qty.el.value);
        const selectedLine = this.pos.get_order().get_selected_orderline();
        if (selectedLine) {
            selectedLine.set_quantity(quantity * this.uom_ratio);
        }
        this.props.close(); 
    }
}
