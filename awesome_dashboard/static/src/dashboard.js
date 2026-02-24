import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

/* ---------------------------
   Dashboard Item
----------------------------*/
class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: { type: Number, optional: true },
    };

    get width() {
        const size = this.props.size || 1;
        return `width: ${18 * size}rem`;
    }
}

/* ---------------------------
   Main Dashboard
----------------------------*/
class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem };

    setup() {
        this.action = useService("action");

        this.state = useState({
            stats: null,
        });

        onWillStart(async () => {
            this.state.stats = await rpc(
                "/awesome_dashboard/statistics",
                {}
            );
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target: "current",
        });
    }
}

/* ---------------------------
   Layout Wrapper
----------------------------*/
class AwesomeDashboardWrapper extends Component {
    static template = "awesome_dashboard.AwesomeDashboardWrapper";
    static components = { Layout, AwesomeDashboard };

    get layoutProps() {
        return {
            controlPanel: {},
            className: "o_dashboard h-100",
        };
    }
}

registry.category("actions").add(
    "awesome_dashboard.dashboard",
    AwesomeDashboardWrapper
);