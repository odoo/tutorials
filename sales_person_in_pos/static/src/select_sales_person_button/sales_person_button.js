import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SelectSalesPersonButton extends Component {
    static template = "sales_person_in_pos.SelectSalesPersonButton";
    static props = ["salesperson?"];

    setup() {
        this.pos = usePos();
    }
}
