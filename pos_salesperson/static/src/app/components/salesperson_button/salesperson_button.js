import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { Component, useState } from "@odoo/owl";


export class SalespersonButton extends Component{
    static template = "pos_salesperson.SalespersonButton";

    setup(){
        this.state = useState({selectedSalesPerson:""})
        this.dialog = useService("dialog");
        this.pos = usePos();
    }

    async chooseSalesPerson(){
        const order = this.pos.get_order();
        const allSalesPersonList = this.pos.models?.["hr.employee"];

        let salesPersonList =  allSalesPersonList.map((s)=>({
            id:s.id,
            item:s,
            label:s.name,
            isSelected:false
        }))

        const selectedSalesPerson = await makeAwaitable(this.dialog, SelectionPopup, {
            list: salesPersonList,
            title: _t("Select the salesperson"),
        });

        if(selectedSalesPerson){
            this.state.selectedSalesPerson = selectedSalesPerson;
            order.salesperson_id = selectedSalesPerson;
        }
    }
}
