# airflow

[![Build Status](https://img.shields.io/travis/infOpen/ansible-role-airflow/master.svg?label=travis_master)](https://travis-ci.org/infOpen/ansible-role-airflow)
[![Build Status](https://img.shields.io/travis/infOpen/ansible-role-airflow/develop.svg?label=travis_develop)](https://travis-ci.org/infOpen/ansible-role-airflow)
[![Updates](https://pyup.io/repos/github/infOpen/ansible-role-airflow/shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-airflow/)
[![Python 3](https://pyup.io/repos/github/infOpen/ansible-role-airflow/python-3-shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-airflow/)
[![Ansible Role](https://img.shields.io/ansible/role/10445.svg)](https://galaxy.ansible.com/infOpen/airflow/)

Ansible role to manage Airflow installation and configuration

First role usage is to manage a single master instance, so I've not manage worker side. If you want, free to do PR to add these features.


## Requirements

This role requires Ansible 2.2 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- Ubuntu Trusty
- Ubuntu Xenial

and use:
- Ansible 2.2.x
- Ansible 2.3.x
- Ansible 2.4.x

### Running tests

#### Using Docker driver

```
$ tox
```

## Role Variables

> **Warning**
> No Fernet key defined on configuration, so set your own before store passwords !

### Default role variables

``` yaml
# Installation vars
airflow_user_name: 'airflow'
airflow_user_group: "{{ airflow_user_name }}"
airflow_user_shell: '/bin/false'
airflow_user_home_path: '/var/lib/airflow'
airflow_user_home_mode: '0700'

airflow_log_path: '/var/log/airflow'
airflow_log_owner: "{{ airflow_user_name }}"
airflow_log_group: "{{ airflow_user_group }}"
airflow_log_mode: '0700'

airflow_pid_path: '/var/run/airflow'
airflow_pid_owner: "{{ airflow_user_name }}"
airflow_pid_group: "{{ airflow_user_group }}"
airflow_pid_mode: '0700'

airflow_virtualenv: "{{ airflow_user_home_path }}/venv"
airflow_python_version: 'python3.4'
airflow_packages:
  - name: 'Cython'
    version: '0.24'
  - name: 'airflow'
    version: '1.7.1.3'
  - name: 'setuptools'
    version: '23.0.0'
airflow_extra_packages:
  - name: 'airflow[crypto]'
airflow_system_dependencies: []


# SERVICES MANAGEMENT
# -----------------------------------------------------------------------------

# Airflow init.d services specific settings
airflow_services_initd:
  - src: "{{ role_path }}/templates/init.d/airflow-webserver.j2"
    dest: '/etc/init.d/airflow-webserver'
    handler: 'Restart airflow-webserver'
  - src: "{{ role_path }}/templates/init.d/airflow-scheduler.j2"
    dest: '/etc/init.d/airflow-scheduler'
    handler: 'Restart airflow-scheduler'

# Airflow upstart services specific settings
airflow_scheduler_respawn_limit_count: 5
airflow_scheduler_respawn_limit_timeperiod: 30
airflow_webserver_respawn_limit_count: 5
airflow_webserver_respawn_limit_timeperiod: 30
is_upstart_managed_system: "{{ _is_upstart_managed_system | default(False) }}"
airflow_services_upstart:
  - src: "{{ role_path }}/templates/upstart/airflow-webserver.conf.j2"
    dest: '/etc/init/airflow-webserver.conf'
    handler: 'Restart airflow-webserver'
  - src: "{{ role_path }}/templates/upstart/airflow-scheduler.conf.j2"
    dest: '/etc/init/airflow-scheduler.conf'
    handler: 'Restart airflow-scheduler'

# Airflow systemd services specific settings
is_systemd_managed_system: "{{ _is_systemd_managed_system | default(False) }}"
airflow_services_systemd:
  - dest: '/etc/systemd/system/airflow-webserver.service'
    handler: 'Restart airflow-webserver'
    options:
      Install:
        WantedBy: 'multi-user.target'
      Service:
        Environment: "PATH={{ airflow_virtualenv ~ '/bin' }}"
        EnvironmentFile: "{{ airflow_paths.files.environment.path }}"
        ExecStart: "{{ airflow_virtualenv ~ '/bin' }}/airflow webserver"
        Group: "{{ airflow_user_group }}"
        PrivateTmp: 'true'
        Restart: 'on-failure'
        RestartSec: '5s'
        Type : 'simple'
        User: "{{ airflow_user_name }}"
      Unit:
        After: 'network.target postgresql.service mysql.service redis.service rabbitmq-server.service'
        Description: 'Airflow webserver daemon'
        Wants: 'postgresql.service mysql.service redis.service rabbitmq-server.service'
  - dest: '/etc/systemd/system/airflow-scheduler.service'
    handler: 'Restart airflow-scheduler'
    options:
      Install:
        WantedBy: 'multi-user.target'
      Service:
        Environment: "PATH={{ airflow_virtualenv ~ '/bin' }}"
        EnvironmentFile: "{{ airflow_paths.files.environment.path }}"
        ExecStart: "{{ airflow_virtualenv ~ '/bin' }}/airflow scheduler"
        Group: "{{ airflow_user_group }}"
        PrivateTmp: 'true'
        Restart: 'always'
        RestartSec: '5s'
        Type : 'simple'
        User: "{{ airflow_user_name }}"
      Unit:
        After: 'network.target postgresql.service mysql.service redis.service rabbitmq-server.service'
        Description: 'Airflow scheduler daemon'
        Wants: 'postgresql.service mysql.service redis.service rabbitmq-server.service'


airflow_services_states:
  - name: 'airflow-webserver'
    enabled: True
    state: 'started'
  - name: 'airflow-scheduler'
    enabled: True
    state: 'started'

# Environment variables file
airflow_paths:
  files:
    environment:
      path: '/etc/default/airflow'

# Databases variables
airflow_manage_database: True
airflow_database_engine: 'mysql'

# Set do_init to false if database already initialized
airflow_do_init_db: True
airflow_do_upgrade_db: True

# Default configuration
airflow_defaults_config:
  core:
    airflow_home: "{{ airflow_user_home_path ~ '/airflow' }}"
    dags_folder: "{{ airflow_user_home_path ~ '/airflow/dags' }}"
    base_log_folder: "{{ airflow_log_path }}"
    remote_base_log_folder: ''
    remote_log_conn_id: ''
    encrypt_s3_logs: False
    executor: 'SequentialExecutor'
    sql_alchemy_conn: 'sqlite:////var/lib/airflow/airflow/airflow.db'
    sql_alchemy_pool_size: 5
    sql_alchemy_pool_recycle: 3600
    parallelism: 32
    dag_concurrency: 16
    dags_are_paused_at_creation: True
    non_pooled_task_slot_count: 128
    max_active_runs_per_dag: 16
    load_examples: False
    plugins_folder: "{{ airflow_user_home_path ~ '/airflow/plugins' }}"
    fernet_key: 'cryptography_not_found_storing_passwords_in_plain_text'
    donot_pickle: False
    dagbag_import_timeout: 30

  operators:
    default_owner: 'Airflow'

  webserver:
    base_url: 'http://localhost:8080'
    web_server_host: '0.0.0.0'
    web_server_port: 8080
    web_server_worker_timeout: 120
    secret_key: 'temporary_key'
    workers: 4
    worker_class: sync
    expose_config: True
    authenticate: False
    filter_by_owner: False
    auth_backend: ''

  email:
    email_backend: 'airflow.utils.email.send_email_smtp'

  smtp:
    smtp_host: 'localhost'
    smtp_starttls: True
    smtp_ssl: False
    smtp_user: 'airflow'
    smtp_port: 25
    smtp_password: 'airflow'
    smtp_mail_from: 'airflow@airflow.com'

  celery:
    celery_app_name: 'airflow.executors.celery_executor'
    celeryd_concurrency: 16
    worker_log_server_port: 8793
    broker_url: 'sqla+mysql://airflow:airflow@localhost:3306/airflow'
    celery_result_backend: 'db+mysql://airflow:airflow@localhost:3306/airflow'
    flower_port: 5555
    default_queue: 'default'

  scheduler:
    job_heartbeat_sec: 5
    scheduler_heartbeat_sec: 5
    statsd_on: False
    statsd_host: 'localhost'
    statsd_port: 8125
    statsd_prefix: 'airflow'
    max_threads: 2

  mesos:
    master: 'localhost:5050'
    framework_name: 'Airflow'
    task_cpu: 1
    task_memory: 256
    checkpoint: False
    failover_timeout: 604800
    authenticate: False
    default_principal: 'admin'
    default_secret: 'admin'

  ldap:
    uri: 'ldaps://<your.ldap.server>:<port>'
    user_filter: 'objectClass=*'
    user_name_attr: 'uid'
    superuser_filter: ''
    data_profiler_filter: ''
    bind_user: ''
    bind_password: ''
    basedn: 'dc=example,dc=com'
    cacert: ''
    search_scope: 'LEVEL'

airflow_user_config: {}
airflow_config: "{{ airflow_defaults_config | combine(airflow_user_config) }}"

# Connections management
airflow_drop_existing_connections_before_add: True
airflow_connections: []

# Variables management
airflow_drop_existing_variables_before_add: True
airflow_variables: []

# Logrotate configuration
airflow_logrotate_config:
  - filename: '/etc/logrotate.d/airflow'
    log_pattern:
      - "{{ airflow_log_path }}/*.log"
    options:
      - 'rotate 12'
      - 'weekly'
      - 'compress'
      - 'delaycompress'
      - "create 640 {{ airflow_log_owner }} {{ airflow_log_group }}"
      - 'postrotate'
      - 'endscript'
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: infOpen.airflow }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro
