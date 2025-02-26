/** @odoo-module **/
import { Component,onWillStart,useState} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboarditem";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout,DashboardItem };

    setup(){
        this.display={
            controlPanel: {},
        }
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();;
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeadView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Lead Management",
            res_model: 'crm.lead',
            views: [[false, 'list'],
                [false, 'form']
            ],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
