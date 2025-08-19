import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SelectEmployeeButton extends Component {
    static template = "pos_orderline_employee.SelectEmployeeButton";
    static props = ["employee?"];
    setup() {
        this.pos = usePos();
    }
}
