import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SalespersonLine extends Component {
    static template = "pos_salesperson.SalespersonLine";
    static props = [
        "close",
        "salesperson",
        "isSelected",
        "onClickUnselect",
        "onClickSalesperson",
    ];

    setup() {
        this.ui = useService("ui");
    }
}
