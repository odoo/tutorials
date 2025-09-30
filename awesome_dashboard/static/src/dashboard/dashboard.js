import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { ConfigDialog } from "./config_dialog/config_dialog";
import { _t } from "@web/core/l10n/translation";
import { user } from "@web/core/user";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }
    setup() {
        this.action = useService("action");
        this.result = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        
        this.state = useState({
            disabledItems: user.settings.disabled_items || [],
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
    
    updateConfigs(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
        user.setUserSettings("disabled_items", this.state.disabledItems)
    }

    openLeads() {
       
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t("CRM Leads"),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false,'list'],[false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

