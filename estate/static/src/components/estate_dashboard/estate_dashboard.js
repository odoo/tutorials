import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./pie_chart/pie_chart";

class EstateDashboard extends Component {
    static template = "estate.EstateDashboard";
    static components = { Layout, PieChart };

    setup() {
        this.action = useService('action');
        this.display = {
            controlPanel: {},
        };
        this.orm = useService("orm");
        this.counts = useState([]);
        onWillStart(async () => {
            this.data = await this.orm.searchRead("estate.property", [], ["state"]);
            this.countStates()
        });
    }

    countStates() {
        this.data.forEach((data) => {
            const state = data.state;
            this.counts[state] = (this.counts[state] || 0) + 1;
        });
    }

    openProperties() {
        this.action.doAction('estate.estate_property_action')
    }

    openChartjs() {
        this.action.doAction({
            'type': "ir.actions.act_url",
            'url': "https://www.chartjs.org/",
            'target': 'new',
        })
    }
}

registry.category("actions").add("estate.dashboard", EstateDashboard);
