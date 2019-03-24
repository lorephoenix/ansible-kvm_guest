kvm_guest
=========

Ansible role that will set up CentOS 7 KVM guests to an existing KVM hypervisor(s).

    $ git clone https://github.com/lorephoenix/ansible-kvm_guest kvm_guest

Requirements
------------

A RHEL derivative GNU/Linux system running a Kernel-based Virtual Machine (KVM) on a x86 hardware that supports virtualization extensions (Intel VT or AMD-V).

The role kvm_guest have some additional requirements. You need to install it before using the role kvm_guest by running the follow command under the role directory kvm_guest.

    $ ansible-galaxy install -r requirements.yml

Our main tasks requires to load a vault file '*vars/vault.yml*' where we specify sensitive variables and values like root passwords, ... (see Role Variables)

    $ ansible-vault create <role_directory>/vars/vault.yml


Role Variables
--------------

#### Other variables for the role

1. vars/secret.yml

A kickstart file requires to have a root password which I recommend to be defined on the vault file '*vars/secret.yml*':

    vault_root_password:    <plaintext password>

The following variables are optional and preferable kept on the vault file '*vars/secret.yml*':

    # When you want to protect your GRUB with a password then set the following line:
    vault_boot_password:    <plaintext password>

    # Local users that needs to be created on our KVM guests.
    vault_local_users:
      - username:           <name of user>
        gecos:              <full name of user>
        password:           <plaintext password>
        sshkeys:
            -               <SSH public key>
    
    # Restrict SSH acces on KVM guest(s) for specific remote IP subnets.
    # If this variable is not specified then SSH access will be allowed 
    # from any host.
    #
    # CIS 3.4.2 Ensure /etc/hosts.allow is configured. 
    #  sshd: ALL
    vault_sshd_hosts_allow:
      - ip:                 <subnet_id>
        subnet_mask:        <subnet mask>


2. defaults/main.yml
   
Default location to store created kickstart file(s) and installation script(s).

    ksroot: '$HOME/ks'
    
    kvm_guest_repo_server: 'http://ftp.belnet.be/mirror/ftp.centos.org/'
    kvm_guest_centos7_url: '{{ kvm_guest_repo_server }}/7/os/x86_64'
    
    kvm_guest_centos7:
        name: centos7
        arch: x86_64
        ostype: linux
        osvariant: rhel7.6
        repo_base_url: '{{ kvm_guest_centos7_url }}'
        url: '{{ kvm_guest_centos7_url }}'
        kickstart: centos7vm.ks



Dependencies
------------

<ul><li>Ansible >= 2.4</li>
    <li>role: kvm_host</li></ul>


Example Playbook
----------------

This is an example playbook:

    - hosts: localhost
      remote_user: ansible
      become: true
      become_method: sudo
      become_user: root
      roles:
        - role: kvm_guest
          # 'profile_<name>' is defined under defaults variable of ansible role
          # kvm_host.
          libvirt_profile: "{{ profile_full }}"
          kvm_guests: "{{ guests }}"

          guests:
          - name: host1
            domainname: example.com
            state: present
            autostart: enabled
            vpcu: 1
            memory: 2048
            # 'kvm_guest_centos<value>' is defined under variable file 'kickstart'
            # within the role kvm_guest.
            os: '{{ kvm_guest_centos7 }}'
            pv_partitions:
            - label: BOOT
              fstype: ext4
              mount_point: /boot
              size: 512
            lv_partitions:
            - label: SWAP
              fstype: swap
              mount_point: swap
              name: lv_swap
              size: 1024
            - label: HOME
              fstype: xfs
              mount_point: /home
              name: lv_home
              size: 2000
            - label: ROOT
              fstype: xfs
              mount_point: /
              name: lv_root
              size: 2000
            - label: TMP
              fstype: tmpfs
              mount_point: /tmp
              name: lv_tmp
              size: 128
            interfaces:
            - device: eth0
              ip: 192.168.0.17
              netmask: 255.255.255.0
              gateway: 192.168.0.1
              bridge: vmbr0


License
-------

MIT

Author Information
------------------

- Christophe Vermeren | [GitHub](https://github.com/lorephoenix) | [Facebook](https://www.facebook.com/cvermeren)

