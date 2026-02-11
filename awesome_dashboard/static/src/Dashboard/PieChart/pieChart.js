import { Component, onWillStart, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";
import { loadJS } from '@web/core/assets';


export class PieChart extends Component {
    static template = "awesome_dashborad.PieChat";

    static props = {
        data: { type: Object },
    }
    setup() {
        this.canvas = useRef("canvas");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });

        useEffect(
            () => {
                this.renderChart();
            },
            () => [this.props.data]
        );
    }

    renderChart() {
        this.chart?.destroy();
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvas.el, {
            type: "pie",
            data: {
                labels,
                datasets: [
                    {
                        data: data,
                    },
                ],
            },
        });
    }
}
