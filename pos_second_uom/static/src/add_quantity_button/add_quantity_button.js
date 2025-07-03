import { Component } from "@odoo/owl"
import { useService } from "@web/core/utils/hooks";
import { AddQuantityDialog } from "../add_quantity_dialog/add_quantity_dialog";


export class AddQuantityButton extends Component {
    static template = "pos_second_uom.AddQuantityButton"

    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    onClick() {
        this.dialogService.add(AddQuantityDialog)
    }
}
