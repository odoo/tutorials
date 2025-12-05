import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { Component, useState } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { SalespersonLine } from "../salesperson_line/salesperson_line";

export class SalespersonList extends Component {
    static template = "point_of_sale.SalespersonList";
    static components = { Dialog, Dropdown, DropdownItem, SalespersonLine };
    static props = {
        salesperson: {
            optional: true,
            type: [{ value: null }, Object],
        },
        getPayload: { type: Function },
        close: { type: Function }
    }

    setup() {
        this.pos = usePos();
        this.ui = useService("ui");
        this.dialog = useService("dialog");
        this.state = useState({
            query: null,
            previousQuery: "",
            currentOffset: 0,
            totalSalespersons: 0,
            isLoading: false,
            query: ''
        });
    }

    getSalesPerson() {
        const salesperson = this.pos.models['hr.employee'].getAll();
        this.state.totalSalespersons = salesperson.length
        return salesperson;
    }

    clickSalesPerson(salesperson) {
        this.props.getPayload(salesperson);
        this.props.close();
    }
}
