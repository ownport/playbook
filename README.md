# playbook

Playbooks for automation, inspired by [Ansible](https://www.ansible.com/), 
an IT automation tool

## Sample

```yaml
---
tasks:

- name: Hello world
  shell: echo "Hello world!"

- name: Get the list of hosts
  shell: cat /etc/hosts
```

## How to use

```sh
$ ./target/playbook run  -p test/resources/simple-playbook.yaml 
2017-04-23 20:16:06,696 (playbook) [INFO] {"status": "SUCCESS", "name": "Hello world"}
2017-04-23 20:16:06,699 (playbook) [INFO] {"status": "SUCCESS", "name": "Get the list of hosts"}
```

## The list of supported actions

### Basic

- shell or command
