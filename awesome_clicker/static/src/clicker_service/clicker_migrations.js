/** @odoo-module **/

export const CURRENT_VERSION = "2.0";

export const migrations = [
    {
        fromVersion: "1.1",
        toVersion: "2.0",
        apply(localState) {
            localState.trees.peachTree = {
                nb_trees: 0,
                fruit: "Peach",
                nb_fruits: 0,
            };
        }
    }
];

export function migrate(localState) {

    if (localState.version != CURRENT_VERSION) {
        migrations.filter((migration) => migration.fromVersion === localState.version && migration.toVersion === CURRENT_VERSION)
            .forEach(migration => { migration.apply(localState); localState.version = CURRENT_VERSION; });
    }

    return localState;
}