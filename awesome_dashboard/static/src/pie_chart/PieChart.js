/** @odoo-module **/

import { Component, xml, onWillStart, onMounted, onWillUnmount, useRef, reactive } from "@odoo/owl";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static props = { 
        caption: String,
        data: Object
    }

    setup() {
        this.canvasRef = useRef("canvas")
        onWillStart(() => 
            loadJS(["/web/static/lib/Chart/Chart.js"])
        );
        onMounted(() => { this.renderChart();        });
        onWillUnmount(() => {
            this.pie.destroy();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        //const color = labels.map((_, index) => getColor(index));
        this.pie = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        //backgroundColor: color,
                    },
                ],
            },
        });
    }

    static template = xml`
    <t t-name="awesome_dashboard.PieChart">
        <div t-att-class="'h-100 ' + props.class" t-ref="root">
            <div class="h-100 position-relative" t-ref="container">
                <canvas t-ref="canvas" />
            </div>
        </div>
    </t>
    `;
    
}
