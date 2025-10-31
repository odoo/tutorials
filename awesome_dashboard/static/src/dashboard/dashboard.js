import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./piechart/piechart";
import { DashboardConfiguration } from "./dashboard_configuration/dashboard_configuration";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        this.statisticsService = useState(useService("awesome_dashboard.statistics"));

        this.allItems = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            hiddenItems: []
        });

        onWillStart(async () => {
            await this.loadHiddenItems();
        });
    }

    get items() {
        const visibleItems = {};
        Object.entries(this.allItems).forEach(([itemId, item]) => {
            if (!this.state.hiddenItems.includes(item.backend_attribute)) {
                visibleItems[itemId] = item;
            }
        });
        return visibleItems;
    }

    async loadHiddenItems() {
        try {
            const config = await this.orm.call('res.users', 'get_dashboard_config', []);
            const hiddenItems = [];
            for (const [itemId, isVisible] of Object.entries(config)) {
                if (!isVisible) {
                    hiddenItems.push(itemId);
                }
            }
            this.state.hiddenItems = hiddenItems;
        } catch (e) {
            console.error("Failed to load dashboard configuration:", e);
            this.state.hiddenItems = [];
        }
    }

    async saveHiddenItems(hiddenItems) {
        try {
            const config = {};
            for (const item of Object.values(this.allItems)) {
                config[item.backend_attribute] = !hiddenItems.includes(item.backend_attribute);
            }
            await this.orm.call('res.users', 'set_dashboard_config', [config]);
            this.state.hiddenItems = hiddenItems;
        } catch (e) {
            console.error("Failed to save dashboard configuration:", e);
        }
    }

    openConfiguration() {
        this.dialog.add(DashboardConfiguration, {
            items: this.allItems,
            hiddenItems: this.state.hiddenItems,
            onSave: async (hiddenItems) => {
                await this.saveHiddenItems(hiddenItems);
            }
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    async openLeads() {
        await this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Leads",
            res_model: 'crm.lead',
            views: [[false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
