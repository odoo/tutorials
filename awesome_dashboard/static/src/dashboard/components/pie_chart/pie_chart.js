import { Component , onWillStart, onMounted, useRef, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component{
    static template = "awesome_dashboard.piechart";

    setup(){
        this.canvasRef = useRef("canvasRef");
        onWillStart(()=> loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(()=> this.renderChart())
        onWillUpdateProps(()=> this.renderChart())
    }

    renderChart(){
        if(this.chart){
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el,{
            type:'pie',
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        data: Object.values(this.props.data)
                    }
                ]
            }
        });
    }

    static props = {
        data: Object
    }
}
