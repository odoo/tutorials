import { Component,onWillStart,useState,useRef,onMounted,useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component{
   
    setup(){
        this.chartRef = useRef('canvas')
        this.statisticsService = useService("awesome_dashboard.statistics");
       this.stats={}
        onWillStart(async ()=>{
           await loadJS("/web/static/lib/Chart/Chart.js")
           this.stats=await this.statisticsService.loadStatistics()
           console.log(this.stats)
           console.log("PICHART onWILL START METHOD")
           
        })

    useEffect( ()=>{
     
       
        if(this.MyPieChart){
            this.MyPieChart.destroy()
        }
        const canvas = this.chartRef.el;//this gets the canvas element
        console.log(canvas)
        if(canvas){
             this.MyPieChart = new Chart(canvas,{"type":"doughnut",
                "data":{"labels":["M size","XL size","S size"],
                "datasets":[
                {"label":"My First Dataset",
                "data":[this.stats.orders_by_size.m,this.stats.orders_by_size.xl,this.stats.orders_by_size.s],
                "backgroundColor":["rgb(255, 99, 132)","rgb(54, 162, 235)","rgb(255, 205, 86)"]}]}})

        }

    })

    }

    static template = "awesome_dashboard.PieChart"; 

}
