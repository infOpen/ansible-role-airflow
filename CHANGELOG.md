# Describe changes between releases

## 0.2.0

This is one of the last 0.x release, role structure is validated and mature

* Add connections management
* Update Molecule to 2.x for role testing
* Update Airlow default version to 1.8.2
* System dependencies are managed by distribution/family dedicated files
* Manage also Debian Jessie and Ubuntu Xenial deployment
* Replace `airflow_default_system_dependencies` by `_airflow_system_dependencies`
* `airflow_system_dependencies` default value is now `_airflow_system_dependencies`
  You can use combine filter to add your packages if needed
* Update core section "home" key to "airflow_home"
