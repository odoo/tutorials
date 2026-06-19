import { Component } from "@odoo/owl";
import { Calculator } from "./calculator/calculator";
import { Formatter } from "./formatter/fromatter";
import { PropertyList } from "./property_list/property_list";
import { OfferList } from "./offer_list/offer_list";
import { UsersList } from "./users_list/users_list";

export class Playground extends Component {
    static template = "vanilla_js.playground";
    static components = { Calculator, Formatter, PropertyList, OfferList, UsersList };
}
