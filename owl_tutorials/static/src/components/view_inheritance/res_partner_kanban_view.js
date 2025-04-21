/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from '@odoo/owl';

class ResPartnerKanbanController extends KanbanController{
    static template = "owl_tutorials.ResPartnerKanbanView"
    setup(){
        super.setup()
        console.log("This is res parnter controller")
        this.action = useService("action")
        this.orm = useService("orm")
        
        onWillStart(async () => {
            this.customerLocation = await this.orm.readGroup("res.partner", [], ['state_id'], ['state_id'])
            this.customerLocations = this.customerLocation.slice(0, -1)
            console.log(this.customerLocations)
        })
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

    selectLocations(state){
        this.model.load({ domain: [['state_id', '=', state[0]]] });
    }
}

export const ResPartnerKanbanView = {
    ...kanbanView,
    Controller: ResPartnerKanbanController,
    buttonTemplate: "owl_tutorials.ResPartnerKanbanView.Buttons"
}

registry.category("views").add("res_partner_kanban_view", ResPartnerKanbanView )
