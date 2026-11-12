import {Component, useState} from "@odoo/owl";
import {Card} from "./card/card";
import {DashboardSettings} from "./dashboard_setting/dashboard_setting";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";

const STORAGE_KEY = "awesome_dashboard_removed_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, Card};

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");

        this.allItems = registry.category("awesome_dashboard").getAll();

        const removedItems = JSON.parse(
            localStorage.getItem(STORAGE_KEY) || "[]"
        );

        this.state = useState({
            removedItems,
            items: this.allItems.filter(
                (item) => !removedItems.includes(item.id)
            ),
        });
    }


    openCustomers() {
        this.action.doAction("base.action_partner_form");
    };

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
        });
    };

    openSettings() {
        this.dialog.add(DashboardSettings, {
            items: this.allItems,
            removedItems: this.state.removedItems,
            onApply: (removedItems) => {
                this.state.removedItems = removedItems;

                this.state.items = this.allItems.filter(
                    (item) => !removedItems.includes(item.id)
                );

                localStorage.setItem(
                    STORAGE_KEY,
                    JSON.stringify(removedItems)
                );
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
