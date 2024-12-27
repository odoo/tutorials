import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "../dashboard_items/dashboard_items";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };


    setup() {
        this.action = useService("action");
    }

    openCustomers() {
        this.action.doAction("base.res_partner_action_kanban");
    }

    openLeads() {
        this.action.doAction({
            name: "Leads",
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }
}
