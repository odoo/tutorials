import { useEffect, useRef } from "@odoo/owl";


export function useAutofocus(name) {
  let ref = useRef(name);
  useEffect(
    (el) => el && el.focus(),
    () => [ref.el]
  );
}
