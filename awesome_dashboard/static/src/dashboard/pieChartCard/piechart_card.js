import { loadJS } from "@web/core/assets"
import { Component, useState, onWillStart, onMounted, useRef, reactive, onWillUnmount, onWillPatch, onWillUpdateProps } from "@odoo/owl";
import { Piechart } from "../piechart/piechart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.pieChartCard";
    static components = { Piechart }

    static props = {
        title: String,
        value: Object
    }
}
