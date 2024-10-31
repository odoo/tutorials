import {useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export function useClick() {
    return useState(useService('awesome_clicker.clicker'))
}