import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SelectSalespersonButton extends Component {
    static template = "pos_salesperson.SelectSalespersonButton";
    static props = ["salesperson?", "class"];
    setup() {
        this.pos = usePos();
    }
}
