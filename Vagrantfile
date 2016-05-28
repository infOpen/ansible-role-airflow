# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

# Ansible version
ANSIBLE_DOWNLOAD_SOURCE = ENV['ANSIBLE_DOWNLOAD_SOURCE'] || "pip"
ANSIBLE_GIT_CHECKOUT = ENV['ANSIBLE_GIT_CHECKOUT'] || "HEAD"
ANSIBLE_GIT_REPOSITORY = ENV['ANSIBLE_GIT_REPOSITORY'] \
                          || "https://github.com/ansible/ansible.git"

# Managed boxes for this role (should have all platform and version defined in
# meta/main.yml)
VMS = {
  :trusty => {
    :box => "ubuntu/trusty64"
  }
}

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  VMS.each_pair do |name, options|

    config.vm.define name do |vm_config|

      # Set proper box
      vm_config.vm.box = options[:box]

      # Update system and install requirements
      vm_config.vm.provision "shell" do |sh|
        if ANSIBLE_DOWNLOAD_SOURCE == 'git'
          sh.inline = "test -d /usr/local/src/ansible \
                        || (sudo apt-get update \
                            && sudo apt-get install python-dev python-pip \
                                                    curl git libffi-dev \
                                                    libssl-dev -y \
                            && sudo pip install paramiko PyYAML Jinja2 \
                                                httplib2 six pytest \
                                                ansible-lint \
                            && cd /usr/local/src \
                            && sudo git clone #{ANSIBLE_GIT_REPOSITORY} \
                            && cd ansible \
                            && sudo git checkout #{ANSIBLE_GIT_CHECKOUT} \
                            && sudo git submodule init \
                            && sudo git submodule update \
                            && sudo make install)"
        else
          sh.inline = "test -f /usr/local/bin/ansible \
                        || (sudo apt-get update \
                            && sudo apt-get install python-dev python-pip \
                                                    curl git libffi-dev \
                                                    libssl-dev -y \
                            && sudo pip install paramiko PyYAML Jinja2 \
                                                httplib2 six pytest ansible \
                                                ansible-lint)"
        end
      end

      # Run pytest tests for filter plugins
      vm_config.vm.provision "shell" do |sh|
        sh.inline = "cd /vagrant \
                      && rm -f tests/__pycache__/*.pyc \
                      && py.test -v"
        sh.privileged = false
      end

      # Use trigger plugin to set environment variable used by Ansible
      # Needed with 2.0 home path change
      vm_config.vm.provision "trigger" do |trigger|
        trigger.fire do
          ENV['ANSIBLE_ROLES_PATH'] = '../'
          ENV['ANSIBLE_ROLE_NAME'] = File.basename(Dir.getwd)
        end
      end

      # Run Ansible linter
      vm_config.vm.provision "shell" do |sh|
        sh.inline = "cd /vagrant && ansible-lint tasks/main.yml"
        sh.privileged = false
      end

      # Run Ansible provisioning
      vm_config.vm.provision "ansible" do |ansible|
        ansible.playbook  = "tests/test_vagrant.yml"
      end

      # Run Serverspec tests
      vm_config.vm.provision "serverspec" do |serverspec|
        serverspec.pattern = 'spec/*_spec.rb'
      end

    end
  end
end
