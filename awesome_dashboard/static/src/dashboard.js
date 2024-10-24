import {Component, useState} from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService } from "@web/core/utils/hooks";
import {DashboardItem} from "./dashboardItem/dashboardItem";
import {PieChart} from "./pieChart/pieChart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart};

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
    }

    openCustomer(){
        this.action.doAction("base.action_partner_form");
    }

    openLeads(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_id: activity.res_id,
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    openSettings() {
          this.action.doAction("base_setup.action_general_configuration");
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);