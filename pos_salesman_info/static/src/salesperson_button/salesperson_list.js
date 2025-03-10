import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Input } from "@point_of_sale/app/generic_components/inputs/input/input";
import { Component, useState } from "@odoo/owl";

export class SalespersonList extends Component {
    static template = "point_of_sale.SalespersonList";
    static components = {Dialog,Input}

    static props = {
        salesperson: {
            optional: true,
            type: [{ value: null }, Object],
        },
        getPayload: { type: Function },
        close: { type: Function },
    };

    setup(){
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.dialog = useService("dialog");
    }
    
    getSalesPerson() {
        const sales_person = this.pos.models["hr.employee"].getAll();
        return sales_person
    }

    async editSalesperson(p = false) {
        const sales_person = await this.pos.editSalesperson(p);
        if (sales_person) { 
            this.clickSalesPerson(sales_person);
        }
    }

    clickSalesPerson(sales_person) {
        this.props.getPayload(sales_person);
        this.props.close();
    }
}
