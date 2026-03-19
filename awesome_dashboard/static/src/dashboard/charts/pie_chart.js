import {
    Component,
    onMounted,
    onWillStart,
    onWillUnmount,
    onWillUpdateProps,
    useRef,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static components = {};
    static props = {
        m: Number,
        s: Number,
        xl: Number,
    };

    setup() {
        this.canvasRef = useRef("canvas_ref");
        const { m, s, xl } = this.props;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            if (!this.canvasRef.el) return;
            const ctx = this.canvasRef.el.getContext("2d");
            if (!ctx) return;

            this.chart = new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: ["M", "S", "XL"],
                    datasets: [
                        {
                            data: [m, s, xl],
                            backgroundColor: ["#4CAF50", "#FF5722", "#9C27B0"],
                        },
                    ],
                },
            });
        });
        onWillUpdateProps((nextProps) => {
            if (!this.chart && !this.canvasRef) return;
            console.log(nextProps);
            this.chart.data.datasets[0].data = [nextProps.m, nextProps.s, nextProps.xl];
            this.chart.update();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }
}
