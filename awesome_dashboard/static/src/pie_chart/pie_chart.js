import {
    Component,
    onWillStart,
    onWillUnmount,
    useRef,
    useEffect,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
      data: { default: {}, type: Object },
    }

    setup() {
        this.rootRef = useRef("root");
        this.canvasRef = useRef("canvas");
        this.containerRef = useRef("container");

        this.chart = null;
        this.tooltip = null;
        this.legendTooltip = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js")
        });

        useEffect(() => {
            this.renderChart();
        });

        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        const labels = Object.keys(this.props.data);
        const values = Object.values(this.props.data);

        const config = {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                  label: "Orders by size",
                  data: values,
                }],
            },
        }

        this.chart = new Chart(this.canvasRef.el, config);
    }
}
