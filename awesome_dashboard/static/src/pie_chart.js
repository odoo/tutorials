import { Component, onWillStart, xml, useRef, useEffect } from "@odoo/owl"
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {

    static template = xml`
        <div>
            <canvas t-ref="canvas"> </canvas>
        </div>
    `

    static props = {
        data : { type : Object }
    }
    
    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));

        useEffect(() => this.renderChart());
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
                    data: values,
                }]
            },
        };
    
        this.chart = new Chart(this.canvasRef.el, config);
    }
}