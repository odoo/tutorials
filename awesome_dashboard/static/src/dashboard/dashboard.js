import { Component, useRef, useState, onWillStart, useEffect, onWillUnmount } from "@odoo/owl";
import { ControlPanel } from "@web/search/control_panel/control_panel"
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { AwesomeCard } from "./dashboard_card";
import { PieChart } from "./pie_chart";
import { DashboardSettingsDialog } from "./dashboard_settings_dialog";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = {
        Layout, AwesomeCard, PieChart,
    };

    static props = {
    };

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        //this.action.doAction("base.crm.lead");
        this.action.doAction({
            type: 'ir.actions.act_window',

            res_model: 'crm.lead',
        });
    }
    static defaultProps = {
        layout: {
            ControlPanel: {},
        },
    };
    openSettings() {
        this.dialog.add(DashboardSettingsDialog, {
            items: registry.category("awesome_dashboard").getAll(),
        });
        console.log("clicked");
    }
    setup() {

        this.dialog = useService("dialog");
        this.dashStat = useService("stat_dash");
        this.action = useService("action");
        this.state = useState(this.dashStat.state);
        const allItems = registry.category("awesome_dashboard").getAll();
        const removedIds = JSON.parse(localStorage.getItem("dashboard_removed_items") || "[]");
        this.items = allItems.filter(item => !removedIds.includes(item.id));

        onWillStart(async () => {
            await this.dashStat.loadStatistics();
        });

        this.data = useState(this.dashStat.state.data);

        onWillStart(async () => {
            await this.dashStat.loadStatistics();
        });

        this.notification = useService("notification");
        this.myService = useService("myService");

        this.components = { ControlPanel }
        this.contentRef = useRef("content");
        this.action = useService("action");

        this.sharedState = useService("shared_state");
        this.sharedState.setValue("hellokey", "hello from service, shared_state, hello key")
        const value = this.sharedState.getValue("hellokey");
        console.log({ "value": value });
        this.sharedState.setValue("newKey", "hello from the newKey");
        console.log({ "newKey": this.sharedState.getValue("newKey") });

        this.showCounterValue = () => {
            //this.notification.add(`counter : ${this.myService.getVal()}`);
            this.myService.getVal();
        }
    }
}
const myService = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            //notification.add(`Tick Tock ${counter++}`);
            counter++;
            console.log(counter);
        }, 1000);

        return {
            getVal() {
                console.log(counter);
                notification.add(`Tick Tock ${counter}`);
            }
        }
    },
};

registry.category("services").add("myService", myService);
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
