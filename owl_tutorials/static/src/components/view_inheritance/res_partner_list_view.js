/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";

class ResPartnerListController extends ListController{
    setup(){
        super.setup()
        console.log("This is res parnter controller")
    }
}

export const ResPartnerListView = {
    ...listView,
    Controller: ResPartnerListController
}

registry.category("views").add("res_partner_list_view", ResPartnerListView )