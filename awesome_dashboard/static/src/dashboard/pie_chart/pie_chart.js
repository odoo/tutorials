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
        data: { type: Object },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this._renderChart();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    _renderChart() {
        if (!this.props.data) {
            return;
        }
        const ctx = this.canvasRef.el.getContext("2d");

        const data = this.props.data;

        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: ["m", "s", "xl"],
                datasets: [
                    {
                        data: [data.m || 0, data.s || 0, data.xl || 0],
                    },
                ],
            },
        });
    }
}
