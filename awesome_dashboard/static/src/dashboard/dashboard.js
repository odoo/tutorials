/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboarditem";
import { PieChart } from "./pieChart/piechart";
import { DashboardSetting } from "./dashboardSetting/dashboard_setting";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart };

    setup() {
        const dashboardItemsRegistry = registry.category("awesome_dashboard");
        this.items = dashboardItemsRegistry.getAll();
        this.dialogService = useService("dialog");


        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.state = useState({ statistics: this.statisticsService.statistics });


        this.displayState = useState({
            disabledItems: [],
            isLoading: true,
        });
        onWillStart(async () => {
            try {
                const fetchedDisabledItems = await rpc("/web/dataset/call_kw/res.users/get_dashboard_settings", {
                    model: 'res.users',
                    method: 'get_dashboard_settings',
                    args: [],
                    kwargs: {},
                });
                this.displayState.disabledItems = fetchedDisabledItems;
            } catch (error) {
                console.error("Error loading initial dashboard settings from server:", error);
                this.displayState.disabledItems = [];
            } finally {
                this.displayState.isLoading = false;
            }
        });
    }

    updateSettings(newUncheckedItems) {
        this.displayState.disabledItems.length = 0;
        this.displayState.disabledItems.push(...newUncheckedItems);
    }

    openSettings() {
        this.dialogService.add(DashboardSetting, {
            items: this.items,
            initialDisabledItems: this.displayState.disabledItems,
            updateSettings: this.updateSettings.bind(this),
        });
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form")
    }

    openLeadsView() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        })
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
