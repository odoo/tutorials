import { Component, xml, onMounted, onWillUnmount, useRef } from "@odoo/owl";

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
