import { Component, onWillStart, useState, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { rpc } from "@web/core/network/rpc";
import { _t } from "@web/core/l10n/translation";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { NumberCard } from "./number/number";
import { PieChartCard } from "./pie_chart/pie_chart_card";
import "./dashboard_item/dashboard_card_items";

class DashboardItemsDialog extends Component {
    static template = xml`
        <Dialog title="labels.title" size="'md'">
            <div class="d-flex flex-column gap-2">
                <p class="mb-2"><t t-esc="labels.question"/></p>
                <t t-foreach="props.items" t-as="item" t-key="item.id">
                    <label class="d-flex align-items-center gap-2">
                        <input
                            type="checkbox"
                            t-att-checked="isChecked(item.id)"
                            t-on-change="(ev) => this.toggleItem(item.id, ev.target.checked)"
                        />
                        <span><t t-esc="item.description"/></span>
                    </label>
                </t>
            </div>
            <t t-set-slot="footer">
                <button class="btn btn-primary" t-on-click="apply"><t t-esc="labels.apply"/></button>
            </t>
        </Dialog>
    `;
    static components = { Dialog };
    static props = {
        items: Array,
        selectedItemIds: Array,
        onApply: Function,
        close: Function,
    };

    setup() {
        this.labels = {
            title: _t("Dashboard items configuration"),
            question: _t("Which cards do you wish to see?"),
            apply: _t("Apply"),
        };
        this.state = useState({
            checkedById: Object.fromEntries(
                this.props.items.map((item) => [item.id, this.props.selectedItemIds.includes(item.id)])
            ),
        });
    }

    isChecked(itemId) {
        return !!this.state.checkedById[itemId];
    }

    toggleItem(itemId, checked) {
        this.state.checkedById[itemId] = checked;
    }

    apply() {
        const removedItemIds = this.props.items
            .filter((item) => !this.state.checkedById[item.id])
            .map((item) => item.id);
        return this.props.onApply(removedItemIds).then(() => this.props.close());
    }
}

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {
        Layout,
        DashboardItem,
        DashboardItemsDialog,
        NumberCard,
        PieChartCard,
    };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");

        const statisticsService = useService("awesome_dashboard.statistics");

        this.labels = {
            customers: _t("Customers"),
            leads: _t("Leads"),
            settings: _t("Settings"),
        };
        this.state = useState({
            removedItemIds: [],
        });
        this.statistics = useState(statisticsService.statistics);
        onWillStart(async () => {
            const [statistics, configuration] = await Promise.all([
                statisticsService.loadStatistics(),
                this.loadDashboardConfiguration(),
            ]);
            return statistics && configuration;
        });
    }

    async loadDashboardConfiguration() {
        const configuration = await rpc("/awesome_dashboard/configuration");
        this.state.removedItemIds = configuration.removed_item_ids || [];
    }

    async saveDashboardConfiguration(removedItemIds) {
        await rpc("/awesome_dashboard/configuration/set", {
            removed_item_ids: removedItemIds,
        });
        this.state.removedItemIds = removedItemIds;
    }

    get items() {
        const removedItemIds = new Set(this.state.removedItemIds);
        return registry
            .category("awesome_dashboard")
            .getAll()
            .filter((item) => !removedItemIds.has(item.id));
    }

    get allItems() {
        return registry.category("awesome_dashboard").getAll();
    }

    openCustomers() {
        this.action.doAction("base.action_partner_customer_form");
    }

    openLeads() {
        this.action.doAction("crm.crm_lead_all_leads"); 
    }

    openSettings() {
        const selectedItemIds = this.allItems
            .filter((item) => !this.state.removedItemIds.includes(item.id))
            .map((item) => item.id);
        this.dialog.add(DashboardItemsDialog, {
            items: this.allItems,
            selectedItemIds,
            onApply: (removedItemIds) => this.saveDashboardConfiguration(removedItemIds),
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);