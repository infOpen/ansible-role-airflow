# airflow

[![Build Status](https://travis-ci.org/infOpen/ansible-role-airflow.svg?branch=master)](https://travis-ci.org/infOpen/ansible-role-airflow)

Ansible role to manage Airflow installation and configuration

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role contains two tests methods :
- locally using Vagrant
- automatically with Travis

### Testing dependencies
- install [Vagrant](https://www.vagrantup.com)
- install [Vagrant serverspec plugin](https://github.com/jvoorhis/vagrant-serverspec)
    $ vagrant plugin install vagrant-serverspec
- install ruby dependencies
    $ bundle install

### Running tests

#### Run playbook and test

- if Vagrant box not running
    $ vagrant up

- if Vagrant box running
    $ vagrant provision

## Role Variables

### Default role variables

## Dependencies

None

## Example Playbook

    - hosts: servers
      roles:
         - { role: infOpen.airflow }

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro

