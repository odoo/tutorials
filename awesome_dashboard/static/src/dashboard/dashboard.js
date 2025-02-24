/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboardItem/dashboard_item";
import { PieChart } from "./pieChart/pie_chart";
import { DashboardItemsDialog } from "./dashboard_item_dialog/dashboard_item_dialog";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        const removedItems = localStorage.getItem("removedItems")?.split(",") ?? [];
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.dialog = useService("dialog");
        this.items = useState(
            registry
                .category("awesome_dashboard")
                .getAll()
                .map((item) => ({
                    ...item,
                    isSelected: !removedItems.find((i) => item.id == i),
                }))
        );
    }

    openCustomerKanban() {
        this.action.doAction("base.action_partner_form");
    }
    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openDialog() {
        this.dialog.add(DashboardItemsDialog, {
            items: this.items.map((item) => ({
                id: item.id,
                description: item.description,
                isSelected: item.isSelected,
            })),
            apply: (removedIds) => {
                localStorage.setItem("removedItems", removedIds?.join(","));
                this.items.forEach((item) => {
                    if (removedIds.includes(item.id)) item.isSelected = false;
                    else item.isSelected = true;
                });
            },
        });
    }
    static components = { Layout, DashboardItem, PieChart };

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
