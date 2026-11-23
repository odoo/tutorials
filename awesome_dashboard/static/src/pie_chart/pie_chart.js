import {
    Component,
    onWillStart,
    onMounted,
    onWillUnmount,
    useRef,
} from "@odoo/owl";

import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        labels: Array,
        values: Array,
    };

    setup() {
        this.canvasRef = useRef("pieChartCanvas");
        this.chart = null;

        // Step 1: Load Chart.js before the component starts rendering.
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        // Step 2: Canvas is now present in the DOM.
        onMounted(() => {
            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    'labels': this.props.labels,
                    datasets: [
                        {
                            data: this.props.values,
                        },
                    ],
                },
            });
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }
}