import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChartTemplate";
    static props = {
        data: Object,
    };

    setup() {
        this.action = useService("action");
        this.canvasRef = useRef("chartCanvas");

        onWillStart(() =>loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(()=> {
            this.renderChart();
        })
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    data: Object.values(this.props.data),
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const clickedIndex = elements[0].index;
                        const clickedSize = Object.keys(this.props.data)[clickedIndex];
                        this.openListView(clickedSize);
                    }
                }
            }
        });
    }

    openListView(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "estate.property",
            views: [[false, 'list']],
            target: "current",
        });
    }
}
