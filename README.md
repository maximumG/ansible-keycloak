Keycloak
========

Role used to install and configure [Keycloak](https://www.keycloak.org/), an Open Source Identity and Access Management product.

By default, the role will:

* Install Keycloak in `/opt/keycloak` directory using keycloak _v11.0.0_
* Install *h2*, *mariadb*, *mssql*, *mysql* and *postgres* Java connectors (*h2* used by default)
* Configure Keycloak as a standalone server (`standalone.xml`)
* Start Keycloak as a SystemD service listenning on `eth0` port 8080 and 8443

Requirements
------------

* Ansible >= 2.8
* RHEL >= 8 or Debian >= 10 (distro with SystemD)

Role Variables
--------------

All variables are defined in `default/main.yml`. Please, check the file for extensive description.

**Default admin account**

The role will create a default admin account for the `Master` realm on first run (user: change-me / pwd: change-me).
You can override the default admin user using `keycloak_admin_user` and `keycloak_admin_password` variables/

**Database drivers**

Supported database are *h2*, *mariadb*, *mssql*, *mysql* and *postgres*. Modify `keycloak_database_driver` with
the driver you want and its subsequents configuration `keycloak_datatase_*`.

```yaml
keycloak_database_driver: mariadb

keycloak_database_server: mariadb.internal
keycloak_database_name: keycloak
keycloak_database_username: root
keycloak_database_password: root
```

:warning:  Ensure that the database exists and that the user has sufficient privileges.

**Java TrustStore**

Keycloak may need a Java truststore to store your internal CA certificates (e.g: LDAP Federation with TLS).

The role will create a truststore as long as you drop your CA certificates in the `files/ca-certificates` folder with
a `*.cer` extension (e.g: `files/ca-certificates/my-own-ca.cer`).

**Keycloak Themes**

The role configures Keycloak to look into `/opt/keycloak/common/themes/` directory by default for Keycloak themes.
By doing so any Keycloak upgrade won't override your own themes.

Dependencies
------------

N/A

Example Playbook
----------------

Install and configure Keycloak 10.0.0 as a SystemD service in `/opt/keycloak/` with an `h2` database
and default admin user on master realm.

```yaml
- hosts: keycloak-server
  roles:
    - keycloak
```

Install and configure Keycloak 10.0.2 as a SystemD service in `/usr/local/share/keycloak` with a `mariadb` database
and using standalone-ha mode.

```yaml
- hosts: keycloak-server
  roles:
    - keycloak
  vars:
    keycloak_version: 10.0.2
    keycloak_destination: /usr/local/share/keycloak
    keycloak_database_driver: mariadb
    keycloak_database_server: mariadb.internal
    keycloak_database_name: keycloak
    keycloak_database_username: root
    keycloak_database_password: root
    keycloak_config_file: standalone-ha.xml
```

Configure Keycloak to listen on interface ens18 port 80/443 and running behind a reverse proxy
with a custom admin user.

```yaml
- hosts: keycloak-server
  roles:
    - keycloak
  vars:
    keycloak_bind_address: '{{ ansible_ens18.ipv4.address }}'
    keycloak_http_port: 80
    keycloak_https_port: 443
    keycloak_reverse_proxy: yes
    keycloak_admin_user: admin
    keycloak_admin_password: supersecret
```

Caveats
-------

Keycloak configuration is based on JBoss-CLI script. Unfortunately, there is no easy way to detect
if the CLI script has changed something or not. All `command` tasks always return a *changed* state
even if no modification has been made.

License
-------

See LICENSE

Author Information
------------------

MaximumG