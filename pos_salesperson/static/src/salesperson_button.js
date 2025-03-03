import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SelectSalesPersonButton extends Component {
    static template = "pos_salesperson.SelectSalesPersonButton";
    static props = ["salesperson?"];

    setup() {
        this.pos = usePos();
    }
}
