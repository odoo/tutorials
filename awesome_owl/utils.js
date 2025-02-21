import { useEffect, useRef } from "@odoo/owl";

export function useAutoFocus(name){
    let ref = useRef(name);
    useEffect(
        (el) => el && el.focus(),
        () => [ref.el]
    );
}
