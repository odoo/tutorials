import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.piechart";
    static props = {
        chart_data: { type: Object },
        clickPie: { type: Function, optional: true },
    };
    setup () {
        this.canvasRef = useRef("dashboard");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart () {
        if (this.chart) {
            this.chart.destroy();
        }
        let labels = [];
        let keys = [];
        for (let size in this.props.chart_data) {
            labels.push(size);
            keys.push(this.props.chart_data[size]);
        }
        console.log("Labels:" + labels);
        console.log("Keys: " + keys);
        const config = {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: keys,
                        label: "Size Distribution",
                    },
                ],
            },
            options: {
                responsive: true,
                // 2. Add the Chart.js onClick handler hook
                onClick: (event, activeElements) => {
                    let elements = activeElements;
                    
                    // Fallback for older/newer Chart.js event signature variations
                    if (!elements || !elements.length) {
                        if (this.chart.getElementsAtEventForMode) {
                            elements = this.chart.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true);
                        } else if (this.chart.getElementAtEvent) {
                            elements = this.chart.getElementAtEvent(event);
                        }
                    }

                    if (elements && elements.length > 0 && this.props.clickPie) {
                        const firstElement = elements[0];
                        // Extract index safely across standard versions (.index vs ._index)
                        const elementIndex = firstElement.index !== undefined ? firstElement.index : firstElement._index;
                        const label = this.chart.data.labels[elementIndex];
                        
                        // 3. Fire the dashboard callback action!
                        this.props.clickPie(label);
                    }
                }
            },
        }
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
