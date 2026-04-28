import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry"
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class EstatePriceTagWidget extends Component{
    static template = "estate.PriceTagWidget"
    static props = {
        ...standardFieldProps,
        currencySymbol: { type: String, optional: true }
    }
    static defaultProps = {
        currencySymbol: "₹"
    }

    get rawValue(){
        return this.props.record.data[this.props.name];
    }

    formattedValue(rawValue){
        if(!rawValue && rawValue !== 0) return "-";
        const numStr = Math.floor(rawValue).toString();
        const lastThree = numStr.slice(-3);
        const remaining = numStr.slice(0,-3);
        const formatted = 
        remaining.length > 0
        ? remaining.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + "," + lastThree
        : lastThree

        return formatted
    }

    get formattedPrice(){
        return this.formattedValue(this.rawValue);
    }

    get priceLabel() {
        const val = this.rawValue;
        if (!val || val <= 0) return "";
        if (val >= 10000000) return `${(val / 10000000).toFixed(2)} Cr`;
        if (val >= 100000) return `${(val / 100000).toFixed(2)} L`;
        return ""
    }

    get symbol() {
        return this.props.currencySymbol;
    }
}

export const estatePriceTagWidget = {
    component: EstatePriceTagWidget,
    supportedTypes: ["float","integer","monetary"],
    extractProps: ({attrs}) => ({
        currencySymbol : attrs.currency_symbol || "₹"
    })
}

registry.category('fields').add('estate_price_tag',estatePriceTagWidget);
