import { Component } from "@odoo/owl";

export class ReferredBy extends Component {
    static template = "pos_referrals.ReferredBy";
    static props = {
        referredby: { type: String, optional: true },
        company_name: { type: String, optional: true },
    };
}
