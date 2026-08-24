import { Component, xml, onMounted, onWillStart, onWillUnmount, useRef } from "@odoo/owl";

import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static props = {
        data: { type: Object },
    };

    static template = xml`
        <div class="w-50 mx-auto">
            <canvas t-ref="canvas"/>
        </div>
    `;

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(() => {
            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [{ data: Object.values(this.props.data) }],
                },
            });
        });

        onWillUnmount(() => {
            this.chart.destroy();
        });
    }
}
