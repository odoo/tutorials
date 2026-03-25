import { Component, useState, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboardItem/dashboardItem";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem };

    static props = {
        statistics: { type: Array, optional: true },
    };

    setup() {
        this.display = {
            controlPanel: {},
        }

        this.action = useService("action");

        const statisticsService = useService("awesome_dashboard.statistics");
        
        this.statistics = useState(statisticsService.statistics);

        this.items = registry.category("awesome_dashboard").getAll();

        this.dialog = useService("dialog");

        this.state = useState({ disabledItemsIds: [] });
    }

    openCustomersKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openCrmLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        });
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            title: _t("Dashboard Items Configuration"),
            items: this.items,
            disabledItemsIds: this.state.disabledItemsIds,
            onApply: (newDisabledItemsIds) => {
                this.state.disabledItemsIds = newDisabledItemsIds;
            },
            size: "medium",
            showFooter: true,
        });
    }
        
}


class ConfigurationDialog extends Component {
    static template = xml`
        <Dialog title="props.title">
            <div class="p-4">
                <p t-esc="this._t('Which cards do you wish to see?')"/>
                <t t-foreach="props.items" t-key="item.id" t-as="item">
                    <CheckBox
                        value="!props.disabledItemsIds.includes(item.id)"
                        t-on-change="() => this.toggleItem(item.id)"
                    >
                        <t t-esc="item.description"/>
                    </CheckBox>
                </t>
            </div>
            <t t-set-slot="footer">
                <button class="btn btn-primary" t-on-click="onApply">Apply</button>
            </t>
        </Dialog>
    `;

    static components = { Dialog, CheckBox };

    setup() {
        this._t = _t;
        this.newDisabledItemsIds = [...this.props.disabledItemsIds];
    }

    toggleItem(itemId) {
        if (this.newDisabledItemsIds.includes(itemId)) {
            this.newDisabledItemsIds = this.newDisabledItemsIds.filter(id => id !== itemId);
        } else {
            this.newDisabledItemsIds = [...this.newDisabledItemsIds, itemId];
        }
    }

    onApply() {
        this.props.onApply(this.newDisabledItemsIds);
        this.props.close();
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
