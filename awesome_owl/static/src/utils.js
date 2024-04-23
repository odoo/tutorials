/** @odoo-module **/

import { useEffect, useRef } from "@odoo/owl";

export function useAutoFocus(inputRef){
    const ref = useRef(inputRef)
    useEffect(
        (el) => {
            el.focus()
        },
        () => [ref.el],
    )
}