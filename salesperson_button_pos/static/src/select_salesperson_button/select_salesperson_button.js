import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
export class SelectSalespersonButton extends Component {
    static template = "point_of_sale.SelectSalespersonButton";
    static props = ["salesperson?"];
    setup() {
        this.pos = usePos();
    }
}
