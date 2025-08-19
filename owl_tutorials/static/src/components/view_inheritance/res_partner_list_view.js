/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

class ResPartnerListController extends ListController{
    setup(){
        super.setup()
        console.log("This is res parnter controller")
        this.action = useService("action")
    }

    openSalesView(){
        console.log("opened sales view")
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customer Sales",
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]]
        })
    }
}

export const ResPartnerListView = {
    ...listView,
    Controller: ResPartnerListController,
    buttonTemplate: "owl_tutorials.ResPartnerListView.Buttons"
}

registry.category("views").add("res_partner_list_view", ResPartnerListView )
