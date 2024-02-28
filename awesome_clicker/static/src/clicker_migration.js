/** @odoo-module */

export const CURRENT_VERSION = 1.1;
export const migrations = [
    {
        fromVersion: 1.0,
        toversion: 1.1,
        apply: (state) => {
            state.trees.peachTree = {
                price: 1500000,
                level: 4,
                produce: "peach",
                purchased: 0,
            };
            state.fruits.peach = 0;
        }
    }
];

export function migrate(localState) {
    if(localState?.version < CURRENT_VERSION) {
        for(const migration of migrations) {
            if(localState.version === migration.fromVersion) {
                migration.apply(localState);
                localState.version = migration.toVersion;
            }
        }
        localState.version = CURRENT_VERSION;
    }

    return localState;
}
