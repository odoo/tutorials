/** @odoo-module **/
import { useRef, useEffect } from "@odoo/owl";

export function useAutofocus(name){
    const ref = useRef(name);

    useEffect(
        (el) => el && el.focus(),
        () => [ref.el]
    );
}