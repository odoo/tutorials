import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard/dashboard_item/dashboard_item"
import { PieChart } from "./dashboard/pie_chart/pie_chart"
import { ConfigurationDialog } from "./dashboard/configuration_dialog/configuration_dialog";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statsService = useService("statisticsService");
        this.state = useState({ 
            statistics: {}, 
            includedItemIds: JSON.parse(browser.localStorage.getItem("dashboard.includedItemIds") || "[]")
        });
        this.dialog = useService("dialog");

        this.state.statistics = this.statsService.statistics;
        
        this.items = registry.category("awesome_dashboard").getAll();
    }

    openCustomersForm() {
        this.action.doAction('base.action_partner_form')
    }

    doAction() {
        console.log("test")
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, "list"], [false, "form"]],
        });
    }

    openConfigurationSettings() {
        console.log('open settings');
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            initialIncludedIds: this.state.includedItemIds,
            onSave: (newIds) => {
                this.state.includedItemIds = newIds;
            }
        })
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
