import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
// import { Prompt } from "@web/core/dialogs/prompt";


export class SelectSalesPersonButton extends Component {
    static template = "pos_salesperson.SelectSalesPersonButton";
    static props = ["salesperson?"];
    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.dialog = useService("dialog");
    }
    onClick(){
        console.log("Clicked");
        const DialogTemp = (this.dialog.add.Prompt, {
            title: "Hello"
        })
        console.log("Current Order :",this.pos.get_order().salesperson_id);
    }
}
