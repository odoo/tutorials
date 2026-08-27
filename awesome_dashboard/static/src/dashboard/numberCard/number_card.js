import { loadJS } from "@web/core/assets"
import { Component, useState, onWillStart, onMounted, useRef, reactive, onWillUnmount, onWillPatch, onWillUpdateProps } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.numberCard";

    static props = {
        title: String,
        value: Number
    }
}
