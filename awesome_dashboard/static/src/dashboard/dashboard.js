/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";

import { AwesomeItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";
import "./statistics_service";

class DashboardConfigDialog extends Component {
    static template = "awesome_dashboard.DashboardConfigDialog";
    static components = { Dialog };
    static props = ["close", "items", "removedItemIds", "onApply"];

    setup() {
        this.state = useState({
            itemStates: {}
        });
        
        // Initialize checkbox states
        this.props.items.forEach(item => {
            this.state.itemStates[item.id] = !this.props.removedItemIds.includes(item.id);
        });
    }

    toggleItem(itemId) {
        this.state.itemStates[itemId] = !this.state.itemStates[itemId];
    }

    apply() {
        const removedItems = [];
        for (const [itemId, isChecked] of Object.entries(this.state.itemStates)) {
            if (!isChecked) {
                removedItems.push(itemId);
            }
        }
        
        // Save to localStorage
        localStorage.setItem('awesome_dashboard_config', JSON.stringify(removedItems));
        
        // Notify parent component
        this.props.onApply();
        
        this.props.close();
    }
}

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, AwesomeItem, PieChart, DashboardConfigDialog };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.statistics = useService("awesome_dashboard.statistics");
        
        // Add state for dashboard configuration
        this.state = useState({
            configVersion: 0 // Used to trigger re-renders when config changes
        });
        
        // Get configuration from localStorage
        this.getRemovedItemIds = () => {
            try {
                const config = localStorage.getItem('awesome_dashboard_config');
                return config ? JSON.parse(config) : [];
            } catch (e) {
                return [];
            }
        };
        
        // Generate all available cards with unique IDs
        this.getAllCards = () => [
            { 
                id: "new_orders",
                title: _t("New Orders This Month"), 
                value: this.statistics.nb_new_orders || 0,
                size: 1 
            },
            { 
                id: "total_sales",
                title: _t("Total Sales This Month"), 
                value: `$${(this.statistics.total_amount || 0).toLocaleString()}`,
                size: 2 
            },
            { 
                id: "avg_quantity",
                title: _t("Avg T-shirts per Order"), 
                value: (this.statistics.average_quantity || 0).toFixed(1),
                size: 1 
            },
            { 
                id: "cancelled_orders",
                title: _t("Cancelled Orders"), 
                value: this.statistics.nb_cancelled_orders || 0,
                size: 1 
            },
            { 
                id: "avg_time",
                title: _t("Avg Processing Time"), 
                value: `${(this.statistics.average_time || 0).toFixed(1)} days`,
                size: 2 
            },
            {
                id: "tshirt_sizes",
                title: _t("T-shirt Sizes Distribution"),
                size: 3,
                isChart: true
            }
        ];

        // Filter cards based on configuration
        this.getCards = () => {
            const removedIds = this.getRemovedItemIds();
            return this.getAllCards().filter(card => !removedIds.includes(card.id));
        };
    }

    onConfigApplied() {
        // Increment version to trigger re-render
        this.state.configVersion++;
    }

    onPieChartSectionClick(size) {
        // Show notification to user
        this.notification.add(
            `Opening orders filtered by t-shirt size: ${size.toUpperCase()}`,
            { type: "info" }
        );
        
        // Open orders list view filtered by t-shirt size
        // Note: This assumes a custom field 'tshirt_size' on sale.order or similar
        // In a real implementation, you'd filter based on your actual data model
        this.action.doAction({
            name: `Orders with T-shirt Size: ${size.toUpperCase()}`,
            res_model: "sale.order",
            type: "ir.actions.act_window",
            views: [
                [false, "list"],
                [false, "form"]
            ],
            // Generic filter - in real implementation, adjust based on your model structure
            domain: [
                '|',
                ['order_line.product_id.name', 'ilike', size],
                ['order_line.product_id.product_tmpl_id.name', 'ilike', size]
            ],
            context: {
                search_default_tshirt_size: size,
                default_tshirt_size: size,
            }
        });
    }


    openDashboardConfig() {
        this.dialog.add(DashboardConfigDialog, {
            items: this.getAllCards(),
            removedItemIds: this.getRemovedItemIds(),
            onApply: () => this.onConfigApplied()
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            name: _t("Leads"),
            res_model: "crm.lead", 
            type: "ir.actions.act_window",
            views: [
                [false, "list"],
                [false, "form"]
            ],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
