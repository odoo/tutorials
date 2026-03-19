# Odoo 19 — Complete Internals Guide
### From `./odoo-bin` to Browser and Back — Every Function, Every Table, Every Flow

---

## HOW TO READ THIS

Read top to bottom. Each chapter builds on the previous one.
By the end you will understand exactly what happens at every step —
which function calls which, what SQL gets executed, and how data moves.

---

# CHAPTER 1 — Boot: `./odoo-bin` to HTTP Server Listening

## The command you run

```bash
./odoo-bin --addons-path=addons,../enterprise,../tutorials -d rd-demo -u estate
```

What each flag does:
```
--addons-path   tells Python where to find addon modules
-d rd-demo      database name to connect to
-u estate       upgrade (install/update) this module
```

## Step 1 — `odoo-bin` (community/odoo-bin:5)

```python
if __name__ == "__main__":
    odoo.cli.main()          # that's it, just calls main()
```

## Step 2 — `main()` (community/odoo/cli/command.py:109)

```python
def main():
    args = sys.argv[1:]

    # parse --addons-path early so we can find addon commands
    if args[0].startswith('--addons-path='):
        config._parse_config([args[0]])   # stores addons path in config
        args = args[1:]

    # default command is 'server' if nothing specified
    command_name = args[0] if args[0] not startswith('-' else 'server'

    command = find_command(command_name)  # finds cli/server.py Server class
    command().run(args)                   # Server().run(args)
```

## Step 3 — `Server.run()` (community/odoo/cli/server.py:125)

```python
class Server(Command):
    def run(self, args):
        config.parser.prog = self.prog
        main(args)               # calls main() in same file
```

## Step 4 — `main(args)` (community/odoo/cli/server.py:95)

```python
def main(args):
    check_root_user()            # warns if running as root
    config.parse_config(args, setup_logging=True)
    # NOW config contains:
    # config['db_name']    = ['rd-demo']
    # config['update']     = {'estate': 1}
    # config['addons_path']= ['addons', '../enterprise', '../tutorials']
    # config['http_port']  = 8069
    # config['workers']    = 0  (threaded mode)

    check_postgres_user()        # exits if db user is 'postgres'
    report_configuration()       # logs version, addons paths

    for db_name in config['db_name']:
        db._create_empty_database(db_name)   # CREATE DATABASE rd-demo if not exists
        config['init']['base'] = True         # force base to load

    setup_pid_file()             # write PID file
    rc = server.start(preload=['rd-demo'], stop=False)
    sys.exit(rc)
```

## Step 5 — `service/server.py start()` (community/odoo/service/server.py:1541)

```python
def start(preload=None, stop=False):
    load_server_wide_modules()   # loads 'base', 'web' immediately
    import odoo.http             # creates odoo.http.root = Application()

    # pick server type:
    if odoo.evented:             server = GeventServer(odoo.http.root)
    elif config['workers']:      server = PreforkServer(odoo.http.root)
    else:                        server = ThreadedServer(odoo.http.root)
    #                                     ^^^ default for development

    rc = server.run(preload=['rd-demo'], stop=False)
    return rc
```

## Step 6 — `ThreadedServer.run()` (community/odoo/service/server.py:660)

```python
def run(self, preload=None, stop=False):
    with Registry._lock:
        self.start(stop=False)          # sets up signals + starts HTTP
        rc = preload_registries(preload) # LOADS ALL MODULES

    self.cron_spawn()                   # starts cron threads

    while self.quit_signals_received == 0:   # main loop, runs forever
        self.process_limit()
        time.sleep(60)                  # wakes on SIGTERM/SIGINT

    self.stop()                         # graceful shutdown
```

`self.start()` (community/odoo/service/server.py:597):
```python
def start(self, stop=False):
    # set signal handlers: SIGINT=shutdown, SIGHUP=reload, SIGUSR1=cache stats
    signal.signal(signal.SIGINT,  self.signal_handler)
    signal.signal(signal.SIGTERM, self.signal_handler)
    signal.signal(signal.SIGHUP,  self.signal_handler)

    if config['http_enable']:
        self.http_spawn()               # starts werkzeug in a thread

def http_spawn(self):                   # community/odoo/service/server.py:589
    self.httpd = ThreadedWSGIServerReloadable(
        self.interface,   # '0.0.0.0'
        self.port,        # 8069
        self.app          # odoo.http.root  (WSGI app)
    )
    Thread(target=self.httpd.serve_forever, daemon=True).start()
    # HTTP server is now listening on port 8069
```

---

# CHAPTER 2 — Module Loading (`-u estate`)

## Step 7 — `preload_registries()` (community/odoo/service/server.py:1490)

```python
def preload_registries(dbnames):
    for dbname in dbnames:             # ['rd-demo']
        threading.current_thread().dbname = dbname
        update_module = config['update']   # {'estate': 1}  from -u flag

        Registry.new(dbname,
            update_module=True,
            upgrade_modules=config['update'],   # {'estate':1}
            install_modules=config['init'],     # {}
        )
```

## Step 8 — `Registry.new()` (community/odoo/orm/registry.py:129)

The Registry is the central object. It holds ALL model classes for a database.

```python
Registry.new('rd-demo', update_module=True, upgrade_modules=['estate']):

    registry = object.__new__(Registry)
    registry.init('rd-demo')
    # registry now has:
    #   registry.models = {}           ← will hold all Model classes
    #   registry._init_modules = set() ← tracks what's loaded
    #   registry.ready = False

    cls.registries['rd-demo'] = registry   # stored globally, one per database

    load_modules(registry,
        update_module=True,
        upgrade_modules=['estate'])

    registry._init = False
    registry.ready = True              # server is now ready for requests
    registry.signal_changes()          # notify other workers via DB
```

## Step 9 — `load_modules()` (community/odoo/modules/loading.py:332)

```python
def load_modules(registry, update_module=False, upgrade_modules=()):

    initialize_sys_path()
    # adds every path in --addons-path to sys.path and odoo.addons.__path__
    # so Python can find: import odoo.addons.estate

    with registry.cursor() as cr:
        cr.execute("SET SESSION lock_timeout = '15s'")

        if not is_initialized(cr):
            modules_db.initialize(cr)
            # creates core tables: ir_module_module, ir_model, ir_model_fields
            # ir_model_access, ir_model_data, ir_ui_view, ir_ui_menu, etc.

        # STEP 1: always load 'base' first
        graph = ModuleGraph(cr, mode='update')
        graph.extend(['base'])
        env = api.Environment(cr, SUPERUSER_ID, {})
        load_module_graph(env, graph, update_module=True)

        # STEP 2: discover all modules, mark estate as 'to upgrade'
        env['ir.module.module'].update_list()
        # scans all addons paths, reads __manifest__.py files
        # inserts missing modules into ir_module_module table

        # mark estate for upgrade
        estate_module = env['ir.module.module'].search([('name','=','estate')])
        estate_module.button_upgrade()
        # sets state = 'to upgrade' in ir_module_module

        # STEP 3: build full graph with all installed modules + estate
        graph2 = ModuleGraph(cr, mode='update')
        graph2.extend(all_installed_modules)
        load_module_graph(env, graph2, update_module=True)
```

## Step 10 — Manifest Reading

Before `load_module_graph` runs, `ModuleGraph` reads every `__manifest__.py`:

```python
# community/odoo/modules/module.py
Manifest.for_addon('estate')
    # looks in each path of odoo.addons.__path__:
    # finds: /home/odoo/odoo19/tutorials/estate/__manifest__.py
    with open(path) as f:
        data = ast.literal_eval(f.read())
    # data = {
    #   'name': 'Real Estate',
    #   'version': '1.0',
    #   'depends': ['base'],
    #   'data': [
    #       'security/ir.model.access.csv',
    #       'views/estate_property_views.xml',
    #       'views/estate_menus.xml',
    #   ],
    #   'installable': True,
    #   'application': True,
    # }
    return Manifest(data)
```

**Dependency resolution** — `graph.extend(['estate'])`:
```
estate depends on → ['base']
base   depends on → []   (root)

Load order: base → estate
```

## Step 11 — `load_module_graph()` (community/odoo/modules/loading.py:107)

This is the core loop. Runs for EACH module in dependency order:

```python
def load_module_graph(env, graph, update_module=False):
    migrations = MigrationManager(cr, graph)

    for index, package in enumerate(graph):
        module_name = package.name         # e.g. 'estate'
        update_operation = (
            'install' if package.state == 'to install' else
            'upgrade' if package.state == 'to upgrade' else  # ← our case
            None
        )

        # ── 1. PRE-MIGRATION ─────────────────────────────
        if update_operation == 'upgrade':
            migrations.migrate_module(package, 'pre')
            # runs scripts/pre-migrate-*.py if they exist

        # ── 2. PYTHON IMPORT ─────────────────────────────
        load_openerp_module('estate')
        # → __import__('odoo.addons.estate')
        # → runs estate/__init__.py  which does: from . import models
        # → runs estate/models/__init__.py  which does: from . import estate_property
        # → runs estate/models/estate_property.py
        # → Python reads class EstateProperty(models.Model):
        #       _name = 'estate.property'
        #       name = fields.Char(required=True)
        #       expected_price = fields.Float(required=True)
        #       ...
        # → MetaModel metaclass fires __init_subclass__
        # → registers class in MetaModel._module_to_models__['estate']

        # ── 3. PRE-INIT HOOK ─────────────────────────────
        if update_operation == 'install':
            pre_init = package.manifest.get('pre_init_hook')
            if pre_init:
                getattr(py_module, pre_init)(env)   # calls your hook function

        # ── 4. REGISTER MODELS ───────────────────────────
        model_names = registry.load(package)
        # for each class in MetaModel._module_to_models__['estate']:
        #   registry.models['estate.property']      = <class EstateProperty>
        #   registry.models['estate.property.type'] = <class EstatePropertyType>
        #   registry.models['estate.property.offer']= <class EstatePropertyOffer>
        # returns ['estate.property', 'estate.property.type', ...]

        # ── 5. CREATE/UPDATE DATABASE TABLES ─────────────
        if update_operation:
            registry._setup_models__(cr, [])      # wire up field descriptors
            registry.init_models(cr, model_names, {'module': 'estate'}, install=True)
            # → for each model: model._auto_init()  ← CREATES TABLES
            # → env['ir.model']._reflect_models()   ← INSERT INTO ir_model
            # → env['ir.model.fields']._reflect_fields() ← INSERT INTO ir_model_fields
            # → registry.check_indexes()            ← CREATE INDEX
            # → registry.check_foreign_keys()       ← ADD FOREIGN KEY

        # ── 6. LOAD DATA FILES ───────────────────────────
        if update_operation == 'install':
            load_data(env, idref, 'init', kind='data', package=package)
            # for each file in manifest['data']:
            #   convert_file(env, 'estate', filename, idref, 'init')

        # ── 7. POST-MIGRATION ────────────────────────────
        migrations.migrate_module(package, 'post')

        # ── 8. TRANSLATIONS ──────────────────────────────
        module._update_translations()

        # ── 9. MARK INSTALLED ────────────────────────────
        module.write({'state': 'installed', 'latest_version': '1.0'})
        env.cr.commit()   # COMMIT after each module

        # ── 10. POST-INIT HOOK ───────────────────────────
        if update_operation == 'install':
            post_init = package.manifest.get('post_init_hook')
            if post_init:
                getattr(py_module, post_init)(env)
```

---

# CHAPTER 3 — Table Creation: Every Field Type to SQL

## Step 12 — `_auto_init()` (community/odoo/orm/models.py:3169)

Called for every model during `registry.init_models()`:

```python
def _auto_init(self):
    cr = self.env.cr
    must_create_table = not sql.table_exists(cr, self._table)
    # self._table = 'estate_property'  (dots replaced with underscores)

    if must_create_table:
        sql.create_model_table(cr, self._table, self._description, [
            (field.name, field.column_type[1] + (" NOT NULL" if field.required else ""), field.string)
            for field in self._fields.values()
            if field.name != 'id' and field.store and field.column_type
        ])
        # SQL:
        # CREATE TABLE estate_property (
        #   id               SERIAL NOT NULL,
        #   name             varchar NOT NULL,
        #   description      text,
        #   postcode         varchar,
        #   expected_price   numeric NOT NULL,
        #   selling_price    numeric,
        #   bedrooms         int4,
        #   state            varchar NOT NULL,
        #   active           bool,
        #   property_type_id int4,      ← Many2one → integer
        #   salesman_id      int4,
        #   buyer_id         int4,
        #   create_uid       int4,
        #   create_date      timestamp,
        #   write_uid        int4,
        #   write_date       timestamp,
        #   PRIMARY KEY(id)
        # )
    else:
        # table exists → check for NEW fields only
        columns = sql.table_columns(cr, self._table)
        for field in self._fields.values():
            if field.store:
                field.update_db(self, columns)   # ALTER TABLE if needed

    self._add_sql_constraints()
    # for each constraint in _sql_constraints:
    # ALTER TABLE estate_property ADD CONSTRAINT ...
```

## Step 13 — Field Types: Python Class → PostgreSQL Column

Every field type is defined in `community/odoo/orm/`:

```
PYTHON FIELD CLASS    FILE                    _column_type           POSTGRESQL COLUMN
─────────────────────────────────────────────────────────────────────────────────────
Boolean               fields_misc.py:22       ('bool','bool')        BOOLEAN
Integer               fields_numeric.py:17    ('int4','int4')        INTEGER
Float                 fields_numeric.py:60    ('numeric','numeric')  NUMERIC
Char(size=255)        fields_textual.py:461   ('varchar',pg_varchar) VARCHAR(255)
Char()                fields_textual.py:461   ('varchar','varchar')  VARCHAR
Text                  fields_textual.py:526   ('text','text')        TEXT
Html                  fields_textual.py:541   ('text','text')        TEXT
Date                  fields_temporal.py:106  ('date','date')        DATE
Datetime              fields_temporal.py:191  ('timestamp','ts...')  TIMESTAMP
Selection             fields_selection.py:20  ('varchar',pg_varchar) VARCHAR
Binary(attachment=F)  fields_binary.py:30     ('bytea','bytea')      BYTEA
Binary(attachment=T)  fields_binary.py:30     None                   NO COLUMN (ir_attachment)
Json                  fields_misc.py:65       ('jsonb','jsonb')      JSONB
Many2one              fields_relational.py:213('int4','int4')        INTEGER + FK
One2many              fields_relational.py:836 None                  NO COLUMN (inverse)
Many2many             fields_relational.py:1198 None                 NO COLUMN (junction table)
```

## Step 14 — `Field.update_db()` (community/odoo/orm/fields.py:1096)

```python
def update_db(self, model, columns):
    if not self.column_type:
        return False      # One2many, Many2many → nothing to do in this table

    column = columns.get(self.name)   # existing column info from PostgreSQL

    self.update_db_column(model, column)    # CREATE or ALTER column
    self.update_db_notnull(model, column)   # handle NOT NULL constraint

    return not column   # True = new column (may need recompute)
```

`update_db_column()` (fields.py:1132):
```python
def update_db_column(self, model, column):
    if not column:
        # column does not exist yet
        sql.create_column(model.env.cr, model._table, self.name, self.column_type[1], self.string)
        # ALTER TABLE estate_property ADD COLUMN expected_price numeric
        return
    if column['udt_name'] == self.column_type[0]:
        return   # already the right type, skip
    self._convert_db_column(model, column)
    # ALTER TABLE estate_property ALTER COLUMN x TYPE new_type USING x::new_type
```

## Step 15 — Many2one: FK Constraint

Many2one stores as `int4` column but also gets a FK:

```sql
-- Column created by update_db_column():
ALTER TABLE estate_property ADD COLUMN property_type_id int4

-- FK created by registry.check_foreign_keys():
ALTER TABLE estate_property
  ADD CONSTRAINT estate_property_property_type_id_fkey
  FOREIGN KEY (property_type_id)
  REFERENCES estate_property_type(id)
  ON DELETE set null    -- from field.ondelete (default for optional M2o)
  -- required M2o defaults to ondelete='restrict'
```

## Step 16 — Many2many: Junction Table

```python
# estate.property  has  tags = fields.Many2many('estate.tag')
# estate.tag table name = 'estate_tag'
# estate.property table = 'estate_property'

# Auto-generated relation table name (alphabetical order):
# 'estate_property_estate_tag_rel'
# column1 = 'estate_property_id'
# column2 = 'estate_tag_id'
```

SQL created:
```sql
CREATE TABLE estate_property_estate_tag_rel (
    estate_property_id  INTEGER NOT NULL
        REFERENCES estate_property(id) ON DELETE cascade,
    estate_tag_id       INTEGER NOT NULL
        REFERENCES estate_tag(id) ON DELETE cascade,
    PRIMARY KEY (estate_property_id, estate_tag_id)
)
```

## Step 17 — One2many: No Column

```python
# offer_ids = fields.One2many('estate.property.offer', 'property_id')
# One2many has NO column in estate_property table
# It works by querying the OTHER table:
# SELECT * FROM estate_property_offer WHERE property_id = <id>
# The 'property_id' column lives on estate_property_offer (the Many2one side)
```

---

# CHAPTER 4 — Data Files: XML to Database Rows

After tables are created, `load_data()` processes `manifest['data']` files.

## Step 18 — `convert_file()` (community/odoo/tools/convert.py:667)

```python
def convert_file(env, module, filename, idref, mode, noupdate):
    ext = os.path.splitext(filename)[1].lower()
    with file_open(pathname, 'rb') as fp:
        if ext == '.csv':   convert_csv_import(env, module, ...)
        elif ext == '.xml': convert_xml_import(env, module, fp, ...)
        elif ext == '.sql': convert_sql_import(env, fp)
```

## Step 19 — XML Parsing: `_tag_record()` (convert.py:336)

For a view XML file like `views/estate_property_views.xml`:

```xml
<record id="estate_property_view_list" model="ir.ui.view">
    <field name="name">estate.property.list</field>
    <field name="model">estate.property</field>
    <field name="arch" type="xml">
        <list string="Properties">
            <field name="name"/>
            <field name="expected_price"/>
            <field name="state"/>
        </list>
    </field>
</record>
```

`_tag_record()` does:
```python
rec_model = 'ir.ui.view'
rec_id    = 'estate_property_view_list'
xid       = 'estate.estate_property_view_list'

res = {
    'name':  'estate.property.list',
    'model': 'estate.property',
    'arch':  '<list string="Properties"><field name="name"/>...</list>',
}

data = {'xml_id': xid, 'values': res, 'noupdate': False}
record = env['ir.ui.view']._load_records([data], update=False)
# → ir.ui.view.create({'name':..., 'model':..., 'arch':...})
# SQL: INSERT INTO ir_ui_view (name, model, arch_db, type, priority, mode, active, ...)
#       VALUES ('estate.property.list', 'estate.property', '<list ...>', 'list', 16, 'primary', true, ...)
#      RETURNING id

self.idref['estate.estate_property_view_list'] = record.id   # 55
```

## Step 20 — `ir_ui_view` Table Structure

```sql
-- What's stored in PostgreSQL for every view:
CREATE TABLE ir_ui_view (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR NOT NULL,      -- 'estate.property.list'
    model        VARCHAR,               -- 'estate.property'
    key          VARCHAR,               -- 'estate.estate_property_view_list'
    priority     INTEGER DEFAULT 16,    -- lower = higher priority
    type         VARCHAR,               -- 'list','form','search','kanban','graph','pivot'
    arch_db      TEXT,                  -- THE ACTUAL XML STORED HERE
    arch_fs      VARCHAR,               -- file path (used in dev-xml mode)
    arch_updated BOOLEAN,               -- True if user modified via Studio
    arch_prev    TEXT,                  -- previous arch (soft reset)
    inherit_id   INTEGER REFERENCES ir_ui_view(id),  -- for extension views
    mode         VARCHAR DEFAULT 'primary',  -- 'primary' or 'extension'
    active       BOOLEAN DEFAULT true,
    create_uid   INTEGER, create_date TIMESTAMP,
    write_uid    INTEGER, write_date  TIMESTAMP
)
```

## Step 21 — `_tag_menuitem()` (convert.py:275)

```xml
<menuitem id="estate_menu_root"
          name="Real Estate"
          web_icon="estate,static/description/icon.png"
          sequence="10"/>

<menuitem id="estate_menu_properties"
          name="Properties"
          parent="estate_menu_root"
          action="estate_property_action"
          sequence="10"/>
```

```python
def _tag_menuitem(self, rec, parent=None):
    values = {
        'parent_id': False,
        'active':    True,
        'sequence':  10,
        'name':      'Real Estate',
        'web_icon':  'estate,static/description/icon.png',
    }

    if rec.get('action'):
        act = self.env.ref('estate.estate_property_action').sudo()
        values['action'] = "ir.actions.act_window,%d" % act.id
        # Reference field: stores model_name,id as string

    data = {'xml_id': 'estate.estate_menu_root', 'values': values, 'noupdate': False}
    menu = self.env['ir.ui.menu']._load_records([data], update=False)
    # SQL: INSERT INTO ir_ui_menu (name, parent_id, sequence, active, action, web_icon, parent_path)
    #       VALUES ('Real Estate', NULL, 10, true, 'ir.actions.act_window,42',
    #               'estate,static/description/icon.png', '/7/')
    #      RETURNING id

    for child in rec.iterchildren('menuitem'):
        self._tag_menuitem(child, parent=menu.id)   # recurse for children
```

## Step 22 — `ir_ui_menu` Table Structure

```sql
CREATE TABLE ir_ui_menu (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR NOT NULL,      -- 'Properties'
    parent_id    INTEGER REFERENCES ir_ui_menu(id),
    parent_path  VARCHAR,              -- '/1/7/'  (materialized path for tree)
    sequence     INTEGER DEFAULT 10,
    active       BOOLEAN DEFAULT true,
    action       VARCHAR,              -- 'ir.actions.act_window,42'
    web_icon     VARCHAR,              -- 'estate,static/description/icon.png'
    create_uid   INTEGER, create_date TIMESTAMP,
    write_uid    INTEGER, write_date  TIMESTAMP
)
-- Many2many for group security:
CREATE TABLE ir_ui_menu_group_rel (
    menu_id INTEGER REFERENCES ir_ui_menu(id),
    gid     INTEGER REFERENCES res_groups(id)
)
```

## Step 23 — `ir.actions.act_window` Table Structure

```xml
<record id="estate_property_action" model="ir.actions.act_window">
    <field name="name">Properties</field>
    <field name="res_model">estate.property</field>
    <field name="view_mode">list,form</field>
    <field name="context">{'search_default_state': 'new'}</field>
</record>
```

```sql
-- ir.actions.act_window inherits from ir.actions via _inherits
-- Two tables are used:

-- Parent table (base action):
INSERT INTO ir_actions (name, type, ...)
VALUES ('Properties', 'ir.actions.act_window', ...)
RETURNING id   → 42

-- Child table (window-specific fields):
INSERT INTO ir_act_window (id, res_model, view_mode, context, domain, ...)
VALUES (42, 'estate.property', 'list,form', '{"search_default_state":"new"}', '[]', ...)
```

## Step 24 — CSV: `ir.model.access`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_estate_property,access_estate_property,model_estate_property,base.group_user,1,1,1,1
```

`convert_csv_import()` → loads via `ir.model.access._load_records()`:
```sql
INSERT INTO ir_model_access (name, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink)
VALUES ('access_estate_property', <model_id>, <group_id>, true, true, true, true)
```

---

# CHAPTER 5 — HTTP Request Handling

Server is running, user opens browser to `http://localhost:8069`.

## Step 25 — WSGI Entry Point (community/odoo/http.py:2758)

Every single HTTP request enters here:

```python
class Application:
    def __call__(self, environ, start_response):
        # environ contains everything about the request:
        # environ['REQUEST_METHOD']  = 'POST'
        # environ['PATH_INFO']       = '/web/dataset/call_kw/estate.property/search_read'
        # environ['HTTP_COOKIE']     = 'session_id=abc123...'
        # environ['wsgi.input']      = <BytesIO with JSON body>

        # reset per-request counters on current thread
        current_thread.query_count = 0
        current_thread.query_time  = 0
        current_thread.perf_t0     = real_time()

        with HTTPRequest(environ) as httprequest:    # werkzeug Request wrapper
            request = Request(httprequest)
            _request_stack.push(request)             # thread-local

            request._post_init()
            # reads session_id cookie → loads session from FileSystemSessionStore
            # session contains: uid=2, db='rd-demo', context={'lang':'en_US'}
            # sets request.db = 'rd-demo'

            if self.get_static_file(httprequest.path):
                response = request._serve_static()    # /estate/static/... files
            elif request.db:
                response = request._serve_db()        # ← normal flow
            else:
                response = request._serve_nodb()      # login page etc.

            return response(environ, start_response)
```

## Step 26 — `_serve_db()` (community/odoo/http.py:2213)

```python
def _serve_db(self):
    cr = None
    try:
        registry = Registry('rd-demo')              # get from global cache
        cr = registry.cursor(readonly=True)          # psycopg2 connection, READ ONLY
        self.registry = registry.check_signaling(cr)
        # check_signaling: if any module was updated, reload registry

        threading.current_thread().dbname = 'rd-demo'

        # create Environment (cr, uid, context)
        self.env = odoo.api.Environment(cr, self.session.uid, self.session.context)
        # self.env['estate.property'] → gives model recordset bound to this cursor + user

        # find which controller to call
        rule, args = self.registry['ir.http']._match(self.httprequest.path)
        # werkzeug routing: '/web/dataset/call_kw/estate.property/search_read'
        # matches route: '/web/dataset/call_kw/<path:path>'
        # rule.endpoint = DataSet.call_kw method

        self._set_request_dispatcher(rule)
        # type='jsonrpc' → dispatcher = JsonRPCDispatcher

        serve_func = self._serve_ir_http(rule, args)
        readonly = rule.endpoint.routing['readonly']
        # search_read has @api.readonly → True
        # create/write/unlink → False (need RW cursor)

        if readonly:
            threading.current_thread().cursor_mode = 'ro'
            return service_model.retrying(serve_func, env=self.env)
        else:
            # close RO cursor, open RW cursor
            cr.close()
            cr = registry.cursor()            # READ-WRITE cursor
            self.env = self.env(cr=cr)
            threading.current_thread().cursor_mode = 'rw'
            return service_model.retrying(serve_func, env=self.env)
    finally:
        self.env = None
        if cr: cr.close()     # always return cursor to pool
```

## Step 27 — `ir.http._match()` (community/odoo/addons/base/models/ir_http.py:205)

```python
@classmethod
def _match(cls, path_info):
    rule, args = request.env['ir.http'].routing_map()\
        .bind_to_environ(request.httprequest.environ)\
        .match(path_info=path_info, return_rule=True)
    return rule, args
    # werkzeug does the actual URL matching
    # '/web/dataset/call_kw/estate.property/search_read'
    # → matches rule '/web/dataset/call_kw/<path:path>'
    # → args = {'path': 'estate.property/search_read'}
    # → rule.endpoint = DataSet.call_kw  (the controller method)
```

---

# CHAPTER 6 — JSON-RPC: Browser to ORM

## Step 28 — JSON Body from Browser

Every ORM call from the browser looks like this:

```json
POST /web/dataset/call_kw/estate.property/search_read
Content-Type: application/json

{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "call",
    "params": {
        "model":  "estate.property",
        "method": "search_read",
        "args":   [[["state", "!=", "sold"]]],
        "kwargs": {
            "fields":  ["name", "expected_price", "state"],
            "limit":   80,
            "offset":  0,
            "context": {"lang": "en_US", "tz": "UTC", "uid": 2}
        }
    }
}
```

## Step 29 — `JsonRPCDispatcher.dispatch()`

```python
# parses JSON body
params = request.get_json_data()['params']
# {'model':'estate.property', 'method':'search_read', 'args':[...], 'kwargs':{...}}

result = endpoint(**params)
# calls: DataSet.call_kw(
#   model='estate.property',
#   method='search_read',
#   args=[[['state','!=','sold']]],
#   kwargs={'fields':[...],'limit':80,'context':{...}},
#   path='estate.property/search_read'
# )

response = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "result": result
})
return Response(response, content_type='application/json')
```

## Step 30 — Controller (community/addons/web/controllers/dataset.py:29)

```python
class DataSet(http.Controller):

    @http.route(['/web/dataset/call_kw', '/web/dataset/call_kw/<path:path>'],
                type='jsonrpc', auth="user", readonly=_call_kw_readonly)
    def call_kw(self, model, method, args, kwargs, path=None):
        # model  = 'estate.property'
        # method = 'search_read'
        # args   = [[['state','!=','sold']]]
        # kwargs = {'fields':[...],'limit':80}

        return call_kw(request.env[model], method, args, kwargs)
        # request.env['estate.property'] → empty recordset of estate.property
        # bound to current cursor + current user
```

## Step 31 — `service.model.call_kw()` (community/odoo/service/model.py:70)

```python
def call_kw(model, name, args, kwargs):
    # model = estate.property()  (empty recordset)
    # name  = 'search_read'
    # args  = [[['state','!=','sold']]]
    # kwargs= {'fields':[...],'limit':80,'context':{...}}

    # SECURITY CHECK: method must be public
    method = get_public_method(model, name)
    # get_public_method() [service/model.py:44]:
    #   if name.startswith('_'):          raise AccessError  (private method)
    #   if method._api_private == True:   raise AccessError  (@api.private)
    #   returns the actual function: BaseModel.search_read

    # search_read is decorated @api.model so no ids needed
    if getattr(method, '_api_model', False):
        recs = model   # use model as-is (no browse needed)

    # pop context from kwargs, apply to recordset
    kwargs = dict(kwargs)
    context = kwargs.pop('context', None) or {}
    recs = recs.with_context(context)
    # creates new env with context merged in

    result = method(recs, *args, **kwargs)
    # = EstateProperty.search_read(
    #     domain=[['state','!=','sold']],
    #     fields=['name','expected_price','state'],
    #     limit=80
    #   )

    # result is list[dict] → returned as-is (not a BaseModel)
    return result
```

## Step 32 — `retrying()` (community/odoo/service/model.py:156)

Wraps every ORM call with concurrency retry logic:

```python
def retrying(func, env):
    for tryno in range(1, 6):           # up to 5 attempts
        try:
            result = func()             # call the ORM method
            if not env.cr._closed:
                env.cr.flush()          # write pending SQL to DB
            break
        except SerializationFailure:    # two transactions conflict
            env.cr.rollback()
            env.transaction.reset()
            env.registry.reset_changes()
            wait = random.uniform(0, 2 ** tryno)   # exponential backoff
            time.sleep(wait)
            # retry...
        except IntegrityError:          # duplicate key etc.
            raise ValidationError("Operation cannot be completed: ...")

    env.cr.commit()                     # final commit
    env.registry.signal_changes()       # notify other workers
    return result
```

---

# CHAPTER 7 — ORM: Python to SQL

## Step 33 — `search_read()` (community/odoo/orm/models.py:5740)

```python
def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    # domain = [['state','!=','sold']]
    # fields = ['name','expected_price','state']
    # limit  = 80

    if not fields:
        fields = list(self.fields_get(attributes=()))  # all fields

    records = self.search_fetch(domain or [], fields, offset=0, limit=80)
    return records._read_format(fnames=fields)
```

## Step 34 — `search_fetch()` (models.py:1383)

```python
@api.model
@api.readonly
def search_fetch(self, domain, field_names=None, offset=0, limit=None, order=None):

    # Step A: build Query object (NO SQL yet, just an AST)
    query = self._search(domain, offset=0, limit=80, order='id')

    if query.is_empty():
        return self.browse()   # optimization: skip if nothing to find

    fields_to_fetch = self._determine_fields_to_fetch(field_names)
    # checks field access rights for each field
    # returns list of Field objects: [Field(name), Field(expected_price), Field(state)]

    return self._fetch_query(query, fields_to_fetch)
```

## Step 35 — `_search()` (models.py:5319)

Builds a Query object — no SQL executed yet:

```python
def _search(self, domain, offset=0, limit=None, order=None):

    # 1. ACCESS CHECK
    self.browse().check_access('read')
    # → SELECT perm_read FROM ir_model_access
    #   WHERE model_id=(SELECT id FROM ir_model WHERE model='estate.property')
    #     AND (group_id IN (2,3,4) OR group_id IS NULL)  -- user's groups
    #   LIMIT 1
    # raises AccessError if no row returned

    domain = Domain(domain)   # [['state','!=','sold']]

    # 2. ADD active=True FILTER (if model has active field)
    domain &= Domain('active', '=', True)
    # domain is now: [['state','!=','sold'], ['active','=',True]]

    # 3. BUILD QUERY OBJECT
    query = Query(self.env, 'estate_property', SQL.identifier('estate_property'))
    query.add_where(domain._to_sql(self, 'estate_property', query))
    # _to_sql converts domain to:
    # estate_property.state != 'sold' AND estate_property.active = true

    # 4. RECORD RULES (row-level security)
    sec_domain = env['ir.rule']._compute_domain('estate.property', 'read')
    # e.g. salesperson can only see their own: [['salesman_id','=',uid]]
    query.add_where(sec_domain._to_sql(...))

    # 5. ORDER/LIMIT/OFFSET
    query.order  = self._order_to_sql('id', query)   # ORDER BY estate_property.id
    query.limit  = 80
    query.offset = 0

    return query    # ← STILL NO SQL EXECUTED
```

## Step 36 — `_fetch_query()` (models.py:3876)

Here the SQL is actually executed:

```python
def _fetch_query(self, query, fields):
    # Separate column fields from non-column fields
    column_fields = [name, expected_price, state]   # have column_type
    other_fields  = []                              # computed non-stored

    # Build SELECT terms
    sql_terms = [SQL.identifier('estate_property', 'id')]
    for field in column_fields:
        sql = self._field_to_sql('estate_property', field.name, query)
        sql_terms.append(sql)

    # ── EXECUTE SQL ──────────────────────────────────────────────────────
    rows = self.env.execute_query(query.select(*sql_terms))
    # execute_query() [environments.py:527]:
    #   env.flush_query(query)     ← flush pending writes that query touches
    #   env.cr.execute(query)      ← psycopg2 sends SQL to PostgreSQL
    #   return env.cr.fetchall()   ← get results back

    # ACTUAL SQL sent to PostgreSQL:
    # SELECT estate_property.id,
    #        estate_property.name,
    #        estate_property.expected_price,
    #        estate_property.state
    # FROM estate_property
    # WHERE estate_property.state != 'sold'
    #   AND estate_property.active = true
    #   AND estate_property.salesman_id = 2    ← from record rule
    # ORDER BY estate_property.id
    # LIMIT 80
    # OFFSET 0

    # rows = [
    #   (1, 'Beach House',    200000.0, 'new'),
    #   (2, 'Mountain Villa', 350000.0, 'offer_received'),
    # ]

    # unzip rows into columns
    column_values = zip(*rows)
    ids = next(column_values)            # (1, 2)
    fetched = self.browse(ids)           # recordset: estate.property(1, 2)

    # ── POPULATE CACHE ───────────────────────────────────────────────────
    for field, values in zip(column_fields, column_values):
        field._insert_cache(fetched, values)
    # cache now contains:
    # env.cache[(estate.property, 'name')]           = {1: 'Beach House',    2: 'Mountain Villa'}
    # env.cache[(estate.property, 'expected_price')] = {1: 200000.0,         2: 350000.0}
    # env.cache[(estate.property, 'state')]          = {1: 'new',            2: 'offer_received'}

    return fetched    # estate.property(1, 2)
```

## Step 37 — `_read_format()` (models.py:3706)

Converts recordset + cache into list of dicts:

```python
def _read_format(self, fnames, load='_classic_read'):
    # self = estate.property(1, 2)
    # fnames = ['name', 'expected_price', 'state']

    data = [(record, {'id': record.id}) for record in self]
    # data = [(record1, {'id': 1}), (record2, {'id': 2})]

    for name in fnames:
        field = self._fields[name]
        convert = field.convert_to_read
        for record, vals in data:
            vals[name] = convert(record[name], record, use_display_name=True)
            # record[name] reads from cache (NO SQL)
            # convert_to_read:
            #   Char    → str as-is
            #   Float   → float as-is
            #   Selection → str (the key, not label)
            #   Many2one → (id, display_name) tuple

    result = [vals for record, vals in data if vals]
    # result = [
    #   {'id': 1, 'name': 'Beach House',    'expected_price': 200000.0, 'state': 'new'},
    #   {'id': 2, 'name': 'Mountain Villa', 'expected_price': 350000.0, 'state': 'offer_received'},
    # ]
    return result
```

## Step 38 — Response back to browser

```
_read_format() → list[dict]
  ↑ returned to call_kw()        → same list[dict]
  ↑ returned to DataSet.call_kw  → same list[dict]
  ↑ returned to JsonRPCDispatcher
      json.dumps({"jsonrpc":"2.0","id":1,"result":[{...},{...}]})
  ↑ retrying() calls env.cr.commit()
  ↑ _serve_db() calls cr.close()  (cursor returned to pool)
  ↑ Application.__call__ returns Response to werkzeug
  werkzeug sends HTTP 200 with JSON body to browser
```

---

# CHAPTER 8 — ORM Write Operations

## Step 39 — `create()` (models.py:4608)

```
RPC call: estate.property.create({'name':'Beach House','expected_price':200000,'state':'new'})
```

```python
def create(self, vals_list):
    # vals_list = [{'name':'Beach House','expected_price':200000,'state':'new'}]

    self.check_access('create')
    # → ir.model.access SQL check for 'create' permission

    new_vals_list = self._prepare_create_values(vals_list)   # [models.py:4764]
    # _add_missing_default_values():
    #   bedrooms default=2     → vals['bedrooms'] = 2
    #   active   default=True  → vals['active']   = True
    #   garden   default=False → vals['garden']   = False
    # strip: id, parent_path, create_uid, write_uid etc.
    # add magic fields:
    #   vals['create_uid']  = 2
    #   vals['create_date'] = '2026-03-19 10:30:00'
    #   vals['write_uid']   = 2
    #   vals['write_date']  = '2026-03-19 10:30:00'

    # classify fields:
    stored   = {'name':'Beach House','expected_price':200000,'state':'new',
                'bedrooms':2,'active':True,'create_uid':2,...}
    inversed = {}     # no inverse fields in these vals
    inherited= {}     # no _inherits on estate.property

    records = self._create(data_list)   # [models.py:4844]
    # ── ACTUAL INSERT ────────────────────────────────────────────────────
    # cr.execute(SQL(
    #   'INSERT INTO estate_property (active,bedrooms,create_date,create_uid,
    #                                  expected_price,name,state,write_date,write_uid)
    #    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    #    RETURNING "id"',
    #   True, 2, '2026-03-19...', 2, 200000.0, 'Beach House', 'new', '2026-03-19...', 2
    # ))
    # → id = 15

    # records = estate.property(15,)

    # populate cache:
    # env.cache[(estate.property,'name')][15]           = 'Beach House'
    # env.cache[(estate.property,'expected_price')][15] = 200000.0
    # env.cache[(estate.property,'state')][15]          = 'new'

    # schedule computed fields:
    records.modified(self._fields, create=True)
    # marks total_area, best_price etc. as "needs recompute"

    self._validate_fields(vals)   # run @api.constrains methods

    # retrying() will call env.cr.flush() + env.cr.commit()

    return records    # estate.property(15,)
    # call_kw() converts this to: 15  (the new id)

# JSON response: {"jsonrpc":"2.0","id":1,"result":15}
```

## Step 40 — `write()` (models.py:4331)

```
RPC call: estate.property.browse([15]).write({'state':'offer_accepted','selling_price':195000})
```

```python
def write(self, vals):
    self.check_access('write')
    # + record rule check: can this user write on record 15?

    # add magic fields
    vals['write_uid']  = 2
    vals['write_date'] = '2026-03-19 10:35:00'

    # for relational fields: mark dependents BEFORE change
    self.modified(fnames_modifying_relations, before=True)

    for field, value in sorted(field_values, key=lambda x: x[0].write_sequence):
        field.write(self, value)
        # puts value in cache for now (batched)

    self.modified(vals)    # mark downstream computed fields

    # ── ACTUAL UPDATE ────────────────────────────────────────────────────
    # _write_multi() [models.py:4521]
    # env.execute_query(SQL("""
    #   UPDATE estate_property
    #   SET selling_price = __tmp.selling_price::numeric,
    #       state         = __tmp.state::varchar,
    #       write_date    = __tmp.write_date::timestamp,
    #       write_uid     = __tmp.write_uid::int4
    #   FROM (VALUES (15, 195000.0, 'offer_accepted', '2026-03-19...', 2))
    #        AS "__tmp"("id", selling_price, state, write_date, write_uid)
    #   WHERE estate_property."id" = "__tmp"."id"
    # """))

    self._validate_fields(vals)   # run @api.constrains

    return True
# JSON response: {"jsonrpc":"2.0","id":1,"result":true}
```

## Step 41 — `unlink()` (models.py:4191)

```python
def unlink(self):
    self.check_access('unlink')

    for func in self._ondelete_methods:
        func(self)    # e.g. archive related offers first

    self.env.flush_all()    # write all pending changes before delete

    self.modified(self._fields, before=True)    # mark dependents

    # ── ACTUAL DELETE ────────────────────────────────────────────────────
    cr.execute(SQL(
        "DELETE FROM estate_property WHERE id IN %s",
        (15,)
    ))
    # PostgreSQL ON DELETE CASCADE removes:
    #   estate_property_offer rows WHERE property_id=15
    #   estate_property_estate_tag_rel rows WHERE estate_property_id=15

    # clean up XML IDs
    Data.search([('model','=','estate.property'),('res_id','in',[15])]).unlink()
    # DELETE FROM ir_model_data WHERE model='estate.property' AND res_id=15

    return True
# JSON response: {"jsonrpc":"2.0","id":1,"result":true}
```

---

# CHAPTER 9 — View Rendering at Runtime

## Step 42 — User Opens the List View

User clicks "Properties" menu in browser.

**JS calls**: `POST /web/dataset/call_kw/estate.property/get_views`
```json
{
    "params": {
        "model":  "estate.property",
        "method": "get_views",
        "args":   [],
        "kwargs": {
            "views": [[false, "list"], [false, "search"]]
        }
    }
}
```

## Step 43 — `get_views()` (community/odoo/addons/base/models/ir_ui_view.py:2893)

```python
def get_views(self, views, options=None):
    result = {}
    result['views'] = {
        v_type: self.get_view(v_id, v_type)
        for [v_id, v_type] in views
    }
    # calls get_view(False, 'list') and get_view(False, 'search')

    result['models'] = {
        model: {'fields': env[model].fields_get(allfields=model_fields)}
        for model, model_fields in models.items()
    }
    return result
```

## Step 44 — `_get_view_cache()` (ir_ui_view.py:3079)

```python
@tools.ormcache('self._get_view_cache_key(view_id, view_type)')
def _get_view_cache(self, view_id=None, view_type='list'):
    arch, view = self._get_view(view_id, view_type)
    arch, models = self._get_view_postprocessed(view, arch)
    return {'arch': arch, 'id': view.id, 'model': view.model, 'models': models}
    # result is cached per (view_id, view_type, lang)
    # next request with same params skips all the work below
```

## Step 45 — `_get_view()` (ir_ui_view.py:2966)

```python
def _get_view(self, view_id=None, view_type='list'):
    IrUiView = self.env['ir.ui.view'].sudo()

    if not view_id:
        # find best matching view
        view_id = IrUiView.default_view('estate.property', 'list')
        # SELECT id FROM ir_ui_view
        # WHERE model='estate.property' AND type='list'
        #   AND mode='primary' AND active=true
        # ORDER BY priority, name, id
        # LIMIT 1
        # → 55

    view = IrUiView.browse(55)
    arch = view._get_combined_arch()
    return arch, view
```

`_get_combined_arch()`:
```python
def _get_combined_arch(self):
    # 1. get base arch
    arch_str = self.arch_db   # reads from ir_ui_view.arch_db column
    # '<list string="Properties"><field name="name"/>...</list>'

    arch = etree.fromstring(arch_str)   # parse to lxml element

    # 2. find all extension views
    extension_views = self.search([
        ('inherit_id', '=', self.id),
        ('mode', '=', 'extension'),
        ('active', '=', True),
    ])
    # SELECT id FROM ir_ui_view WHERE inherit_id=55 AND mode='extension' AND active=true

    # 3. apply each extension in priority order
    for child_view in extension_views:
        child_arch = etree.fromstring(child_view.arch_db)
        arch = apply_inheritance_specs(arch, child_arch)
        # applies XPath: <xpath expr="//field[@name='name']" position="after">...</xpath>
        # modifies the lxml tree in-place

    return arch
```

## Step 46 — Response to Browser

```json
{
    "result": {
        "views": {
            "list": {
                "arch": "<list string=\"Properties\"><field name=\"name\"/><field name=\"expected_price\"/><field name=\"state\"/></list>",
                "id": 55,
                "model": "estate.property"
            },
            "search": {
                "arch": "<search><field name=\"name\"/><filter name=\"state_new\" domain=\"[['state','=','new']]\" string=\"New\"/></search>",
                "id": 56
            }
        },
        "models": {
            "estate.property": {
                "fields": {
                    "name":           {"type":"char",      "string":"Title",          "required":true},
                    "expected_price": {"type":"float",     "string":"Expected Price", "required":true},
                    "state":          {"type":"selection", "string":"Status",
                                       "selection":[["new","New"],["offer_received","Offer Received"],["sold","Sold"]]},
                    "property_type_id": {"type":"many2one","string":"Property Type","relation":"estate.property.type"}
                }
            }
        }
    }
}
```

**JS then calls `web_search_read`** → goes through ORM flow (Chapter 7) → gets data → renders table.

---

# CHAPTER 10 — Recordset API

The recordset is the core Python object you work with every day.
`estate.property(1, 2, 3)` means a recordset of 3 estate.property records.

```python
# ── CREATING RECORDSETS ──────────────────────────────────────────────────────

env['estate.property']              # empty recordset, no SQL
env['estate.property'].browse(15)   # recordset(15,), no SQL
env['estate.property'].browse([1,2,3])  # recordset(1,2,3), no SQL

env['estate.property'].search([('state','=','new')])
# → SELECT ... WHERE state='new'  → recordset of matching ids

env.ref('estate.estate_menu_root')
# → SELECT res_id FROM ir_model_data WHERE module='estate' AND name='estate_menu_root'
# → ir.ui.menu(7,)

# ── ENVIRONMENT MODIFICATION ─────────────────────────────────────────────────

records.sudo()
# new env with uid=1 (superuser), bypasses ALL access checks
# use carefully

records.with_user(uid)
# new env with different user

records.with_context(key=value)
# adds to context dict
# env['estate.property'].with_context(lang='fr_FR')
# → all field reads return translated values

records.with_env(other_env)
# completely swap environment

# ── FILTERING ────────────────────────────────────────────────────────────────

records.filtered(lambda r: r.state == 'new')
# iterates self in Python, returns matching records
# reads from cache (may trigger SQL if not cached)
# → estate.property(1, 3)

records.filtered('active')
# shorthand: lambda r: r['active']

records.filtered_domain([('state','=','new')])
# applies domain filter in Python (no SQL)

# ── MAPPING ──────────────────────────────────────────────────────────────────

records.mapped('name')
# → ['Beach House', 'Mountain Villa']

records.mapped('property_type_id.name')
# follows relational chain:
# 1. fetches property_type_id for each record
# 2. fetches name on the comodel records
# → ['Apartment', 'House']

records.mapped(lambda r: r.expected_price * 1.1)
# → [220000.0, 385000.0]

# ── SORTING ──────────────────────────────────────────────────────────────────

records.sorted('expected_price')
# → sorted ascending by field value

records.sorted('expected_price', reverse=True)
# → sorted descending

records.sorted(key=lambda r: (r.state, r.expected_price))
# → multi-key sort

# ── SET OPERATIONS ───────────────────────────────────────────────────────────

r1 | r2    # union (deduplicated)
r1 & r2    # intersection
r1 - r2    # difference
r1 + r2    # concatenate (may have duplicates)
15 in r1   # True if record with id=15 is in recordset
len(r1)    # number of records

# ── EXISTENCE ────────────────────────────────────────────────────────────────

records.exists()
# SELECT id FROM estate_property WHERE id IN (1,2,3)
# returns only records that still exist in DB
# useful after possible deletion by other transactions

# ── NEW RECORD (virtual) ─────────────────────────────────────────────────────

new_rec = self.new({'name': 'Test', 'expected_price': 100000})
# creates record in cache only, no INSERT
# used for onchange evaluation and precomputed fields
```

---

# CHAPTER 11 — All Tables Created by a Typical Addon

```
CORE TABLES (created by 'base' module on first run):
┌─────────────────────────┬──────────────────────────────────────────────┐
│ ir_model                │ registry of all models (estate.property etc) │
│ ir_model_fields         │ all fields of each model                     │
│ ir_model_access         │ perm_read/write/create/unlink per group      │
│ ir_model_data           │ XML IDs: module.xml_id → model + res_id      │
│ ir_rule                 │ record-level access rules (domain per group)  │
│ ir_ui_view              │ ALL view XMLs (arch_db column holds XML)      │
│ ir_ui_menu              │ menu items tree                               │
│ ir_actions              │ base actions (parent of act_window etc)       │
│ ir_act_window           │ act_window actions (inherits ir_actions)      │
│ ir_act_server           │ server actions                                │
│ res_groups              │ security groups                               │
│ res_users               │ users                                         │
│ res_partner             │ partners (base of users, customers etc)       │
│ ir_module_module        │ installed/available modules list              │
└─────────────────────────┴──────────────────────────────────────────────┘

YOUR ADDON TABLES (created by estate module):
┌───────────────────────────────────────┬──────────────────────────────────┐
│ estate_property                       │ main model                       │
│ estate_property_type                  │ property types                   │
│ estate_property_offer                 │ offers on properties             │
│ estate_tag                            │ tags                             │
│ estate_property_estate_tag_rel        │ M2m junction: property ↔ tags   │
└───────────────────────────────────────┴──────────────────────────────────┘
```

---

# CHAPTER 12 — The Complete Story (One Page)

```
YOU RUN: ./odoo-bin --addons-path=... -d rd-demo -u estate
                │
                ▼
        odoo-bin → cli/command.py:109 main()
        find 'server' command → cli/server.py:95 main()
        config.parse_config()  ← stores all flags
        db._create_empty_database('rd-demo')
        service/server.py:1541 start()
        ThreadedServer created
        werkzeug thread spawned → port 8069 listening  ✓
                │
                ▼
        preload_registries(['rd-demo'])
        Registry.new('rd-demo')  [orm/registry.py:129]
        load_modules()  [modules/loading.py:332]
                │
                ▼
        FOR EACH module (base, mail, ..., estate):
          read __manifest__.py → name, depends, data files
          resolve dependency order via ModuleGraph
          Python import → class definitions run
          MetaModel registers all Model classes
          registry.load() → registry.models['estate.property'] = <class>
          _auto_init() → CREATE TABLE estate_property (...)
          field.update_db() → ALTER TABLE ADD COLUMN per field
            Char/Text/Html  → VARCHAR/TEXT
            Integer         → INTEGER (int4)
            Float           → NUMERIC
            Boolean         → BOOLEAN
            Date/Datetime   → DATE/TIMESTAMP
            Selection       → VARCHAR
            Many2one        → INTEGER + FK constraint
            One2many        → NO COLUMN (inverse of M2o)
            Many2many       → NO COLUMN + CREATE junction table
          convert_file() for each data file:
            XML: _tag_record()   → ir.ui.view.create()   → INSERT INTO ir_ui_view
            XML: _tag_record()   → ir.actions.act_window.create() → INSERT INTO ir_act_window
            XML: _tag_menuitem() → ir.ui.menu.create()   → INSERT INTO ir_ui_menu
            CSV: ir.model.access → INSERT INTO ir_model_access
          module.state = 'installed' → COMMIT  ✓
                │
                ▼
        SERVER READY. Registry loaded. HTTP listening on :8069.
                │
                ▼
        USER OPENS BROWSER → GET /odoo/estate
        Application.__call__(environ)  [http.py:2758]
        Request._serve_db()  [http.py:2213]
          Registry('rd-demo').cursor()  → psycopg2 connection
          Environment(cr, uid=2, context)
          ir.http._match(path)  → werkzeug finds controller
          JsonRPCDispatcher
                │
                ▼
        JS: POST /web/dataset/call_kw/estate.property/get_views
        get_views() → _get_view_cache() [ormcache]
          SELECT id FROM ir_ui_view WHERE model=... AND type='list'
          SELECT arch_db FROM ir_ui_view WHERE id=55
          apply extension views with lxml XPath
          postprocess: access checks, modifiers
          fields_get(): field metadata
        → JSON: arch XML + field definitions back to browser
                │
                ▼
        JS: POST /web/dataset/call_kw/estate.property/web_search_read
        DataSet.call_kw() → service.call_kw() → Model.search_read()
          search_fetch()
            _search(): access check + record rules → Query object
            _fetch_query():
              env.execute_query() → cr.execute(SELECT ... WHERE ... LIMIT 80)
              PostgreSQL returns rows
              field._insert_cache() → values in env.cache
          _read_format(): reads cache → list[dict]
        retrying(): env.cr.flush() + env.cr.commit()
        → JSON: [{"id":1,"name":"Beach House",...}, ...]
                │
                ▼
        OWL JS renders:
          ListRenderer walks arch XML
          each <field name="X"> → picks widget by type:
            char      → <input type="text">
            float     → <input type="number">
            selection → <select>
            many2one  → <input> with autocomplete (name_search RPC)
            boolean   → <input type="checkbox">
          fills values from search_read result  ✓
                │
                ▼
        USER CREATES A RECORD → clicks Save
        POST /web/dataset/call_kw/estate.property/web_save
        Model.create([{name, expected_price, state}])
          check_access('create') → ir.model.access SQL
          _prepare_create_values() → add defaults + magic fields
          _create():
            cr.execute(INSERT INTO estate_property (...) VALUES (...) RETURNING id)
            → id = 15
            cache populated
            computed fields scheduled for recompute
          _validate_fields() → @constrains run
          env.cr.flush() + env.cr.commit()
        → JSON: {"result": 15}  ✓
                │
                ▼
        USER EDITS A RECORD → clicks Save
        Model.write({'state':'offer_accepted','selling_price':195000})
          check_access('write') + record rule check
          field.write() → cache updated
          _write_multi():
            UPDATE estate_property SET state=..., selling_price=...
            WHERE id=15
          _validate_fields() → @constrains run
          env.cr.commit()
        → JSON: {"result": true}  ✓
                │
                ▼
        USER DELETES A RECORD
        Model.unlink()
          check_access('unlink')
          @ondelete methods run
          env.flush_all()
          DELETE FROM estate_property WHERE id IN (15,)
          ir_model_data cleanup
          ir_attachment cleanup
          env.cr.commit()
        → JSON: {"result": true}  ✓
```

---

# KEY FILES REFERENCE

```
STARTUP
  community/odoo-bin:5                                  entry point
  community/odoo/cli/command.py:109                     main() CLI
  community/odoo/cli/server.py:95                       Server.main()
  community/odoo/service/server.py:1541                 start()
  community/odoo/service/server.py:589                  http_spawn() werkzeug
  community/odoo/service/server.py:660                  ThreadedServer.run()
  community/odoo/service/server.py:1490                 preload_registries()

MODULE LOADING
  community/odoo/orm/registry.py:129                    Registry.new()
  community/odoo/orm/registry.py:366                    registry.load() register models
  community/odoo/orm/registry.py:723                    registry.init_models()
  community/odoo/modules/loading.py:332                 load_modules()
  community/odoo/modules/loading.py:107                 load_module_graph()
  community/odoo/modules/module.py                      Manifest.for_addon()

TABLE CREATION
  community/odoo/orm/models.py:3169                     _auto_init() CREATE TABLE
  community/odoo/orm/fields.py:1096                     Field.update_db()
  community/odoo/orm/fields.py:1132                     Field.update_db_column() ALTER TABLE
  community/odoo/orm/fields.py:1150                     Field.update_db_notnull() NOT NULL

FIELD TYPES
  community/odoo/orm/fields_numeric.py:17               Integer
  community/odoo/orm/fields_numeric.py:60               Float
  community/odoo/orm/fields_textual.py:461              Char
  community/odoo/orm/fields_textual.py:526              Text
  community/odoo/orm/fields_textual.py:541              Html
  community/odoo/orm/fields_misc.py:22                  Boolean
  community/odoo/orm/fields_misc.py:65                  Json
  community/odoo/orm/fields_temporal.py:106             Date
  community/odoo/orm/fields_temporal.py:191             Datetime
  community/odoo/orm/fields_selection.py:20             Selection
  community/odoo/orm/fields_relational.py:213           Many2one
  community/odoo/orm/fields_relational.py:836           One2many
  community/odoo/orm/fields_relational.py:1198          Many2many

DATA FILE PARSING
  community/odoo/tools/convert.py:667                   convert_file()
  community/odoo/tools/convert.py:336                   _tag_record() → create()
  community/odoo/tools/convert.py:275                   _tag_menuitem() → ir.ui.menu
  community/odoo/tools/convert.py:469                   _tag_template() → ir.ui.view

VIEW SYSTEM
  community/odoo/addons/base/models/ir_ui_view.py:139   IrUiView model definition
  community/odoo/addons/base/models/ir_ui_view.py:2893  get_views() RPC entry
  community/odoo/addons/base/models/ir_ui_view.py:2966  _get_view() find + combine
  community/odoo/addons/base/models/ir_ui_view.py:3079  _get_view_cache() ormcache
  community/odoo/addons/base/models/ir_ui_menu.py:16    IrUiMenu model definition

HTTP + RPC
  community/odoo/http.py:2758                           Application.__call__() WSGI
  community/odoo/http.py:2213                           _serve_db()
  community/odoo/addons/base/models/ir_http.py:205      ir.http._match() routing
  community/addons/web/controllers/dataset.py:28        DataSet.call_kw() controller
  community/odoo/service/model.py:70                    service.call_kw()
  community/odoo/service/model.py:44                    get_public_method()
  community/odoo/service/model.py:137                   execute_cr()
  community/odoo/service/model.py:156                   retrying()

ORM READ
  community/odoo/orm/models.py:5740                     search_read()
  community/odoo/orm/models.py:1383                     search_fetch()
  community/odoo/orm/models.py:5319                     _search() → Query object
  community/odoo/orm/models.py:3876                     _fetch_query() → SQL + cache
  community/odoo/orm/models.py:3706                     _read_format() → list[dict]
  community/odoo/orm/models.py:3466                     read()
  community/odoo/orm/environments.py:527                execute_query() → cr.execute()

ORM WRITE
  community/odoo/orm/models.py:4608                     create()
  community/odoo/orm/models.py:4764                     _prepare_create_values()
  community/odoo/orm/models.py:4844                     _create() → INSERT SQL
  community/odoo/orm/models.py:4331                     write()
  community/odoo/orm/models.py:4521                     _write_multi() → UPDATE SQL
  community/odoo/orm/models.py:4191                     unlink() → DELETE SQL
```

---

*All file paths are relative to `/home/odoo/odoo19/`*
*All line numbers verified against Odoo 19 community source*
