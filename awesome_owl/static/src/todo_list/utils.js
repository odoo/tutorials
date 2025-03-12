import { useEffect, useRef } from "@odoo/owl"

export function useAutoFocus(name) {
    const ref = useRef(name);
    useEffect(
        (el) => el && el.focus(),
        () => [ref.el]
    );
}
