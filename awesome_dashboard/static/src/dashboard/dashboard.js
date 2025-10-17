/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboardItem/dashboardItem";
import { ConfigDialog } from "./configDialog/configDialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, ConfigDialog };

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.dashboardData = useState(this.statistics.stats);
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");

        this.state = useState({
            hiddenIds: JSON.parse(localStorage.getItem("hidden_dashboard_items") || "[]")
        });
                
    }

    get filteredItems(){
        return this.items.filter(item => !this.state.hiddenIds.includes(item.id));
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    openDialogView() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            hiddenIds: this.state.hiddenIds,
            onApply: (hiddenIds) => {this.state.hiddenIds = hiddenIds },
        });
    }

}

registry.category("lazy_components").add("dashboard", AwesomeDashboard);
