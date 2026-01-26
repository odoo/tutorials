const MIGRATIONS = [
    {
        version_from: "1.0",
        version_to: "1.1",
        apply(local_state) {
            console.log("Migrating from 1.0 to 1.1");
            Object.assign(local_state.trees, {
                peach: {
                    name: "Peach Tree",
                    fruit_name: "Peach",
                    quantity: 0,
                    price: 1000000,
                    fruits: 0,
                    level_required: 4,
                }
            });
        },
    }
]

export function migrate(local_state, target_version) {
    while (local_state.version != target_version) {
        let migration = MIGRATIONS.find(update => update.version_from === local_state.version);
        migration.apply(local_state);
        local_state.version = migration.version_to;
    }
}
