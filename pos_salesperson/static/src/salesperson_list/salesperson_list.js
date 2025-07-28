import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class SalespersonList extends Component {
    static template = "pos_salesperson.SalespersonList";
    static components = { Dialog };
    static props = {
        salesperson: {
            optional: true,
            type: [{ value: null }, Object],
        },
        getPayload: { type: Function },
        close: { type: Function },
    };

    setup() {
        this.pos = usePos();
    }

    getSalesperson() {
        return this.pos.models['hr.employee'].getAll();
    }

    setSalesperson(salesperson) {
        this.props.getPayload(salesperson);
        this.props.close();
    }

    get isSelected() {
        return this.props.salesperson && this.props.salesperson.id === this.salesperson.id;
    }
}
