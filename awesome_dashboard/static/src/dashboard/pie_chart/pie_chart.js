import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: { },
        size: { type: Number, optional: true },
    };

    setup() {
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        this.ctx = useRef("pieChart");
        this.chart = null;
        onMounted(() => {
            if (this.chart) {
                this.chart.destroy();
            }
            const dataset = {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        data: Object.values(this.props.data),
                    },
                ],
            };
            this.chart = new Chart(this.ctx.el, { type: "pie", data: dataset });
        });
    }
}
