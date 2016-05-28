require 'serverspec'

if ENV['TRAVIS']
    set :backend, :exec
end

describe 'airflow Ansible role' do

    # Declare variables
    packages = Array[]

    if ['debian', 'ubuntu'].include?(os[:family])
        packages = Array[ 'apt' ]
    end

    it 'install role packages' do
        packages.each do |pkg_name|
            expect(package(pkg_name)).to be_installed
        end
    end
end

