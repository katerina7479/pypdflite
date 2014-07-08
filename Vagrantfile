VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.box = "ubuntu-trusty"
    config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

    config.vm.network :private_network, ip: "192.168.56.11"
    config.ssh.forward_agent = true

    config.vm.synced_folder "./", "/projects", :nfs => true

    config.vm.provider :virtualbox do |v|
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--memory", 512]
        v.customize ["modifyvm", :id, "--name", "dupexi-box"]
    end

    #config.vm.network :forwarded_port, guest: 80, host: 8080

    config.vm.provision "shell", path: "script.sh"
end