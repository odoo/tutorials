import { Component, onWillStart,useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { ConfigDialog } from "./config_dialog";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }
    setup() {
        this.action = useService("action");
        this.result = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        // retreive disabled items
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledItems")?.split(",") || []
        });
    }
    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }
    openConfigs() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfigs: this.updateConfigs.bind(this),
        });
    }
    // update the list of disabeled items
    updateConfigs(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    openLeads() {
       
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('CRM Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false,'list'],[false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

