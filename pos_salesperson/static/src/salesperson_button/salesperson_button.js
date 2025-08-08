import { Component, markRaw } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SalespersonButton extends Component {
    static template = 'pos_salesperson.SelectSalespersonButton';
    setup() {
        this.pos = usePos();
    }

    get salesperson() {
        return this.pos.get_order()?.get_salesperson();
    }
}
