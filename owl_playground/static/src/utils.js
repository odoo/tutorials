/** @odoo-module **/


import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(Input) {
    const inputRef = useRef(Input);
    onMounted(() => inputRef.el.focus());
}