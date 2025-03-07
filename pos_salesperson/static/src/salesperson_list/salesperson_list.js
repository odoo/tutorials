import { Component, onWillStart, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";

export class SalespersonList extends Component {
    static template = "pos_salesperson.SalespersonList";
    static components = { Dialog };
    static props = ["salesperson?", "getPayload", "close"];

    setup() {
        this.dialog = useService("dialog");
        this.pos = usePos();
        this.orm = useService("orm");
    }

    getSalespersons() {
        const salespersons = this.pos.models["hr.employee"].getAll();
        return salespersons;
    }

    selectSalesperson(salesperson) {
        if (!salesperson || salesperson.id == this.props.salesperson?.id) {
            this.props.getPayload(false);
        } else {
            this.props.getPayload(salesperson);
        }
        this.props.close();
    }

    discardDialog() {
        this.props.getPayload(this.props.salesperson ?? false);
        this.props.close();
    }
}
