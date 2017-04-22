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
$ ./target/playbook run -l INFO -p test/resources/simple-playbook.yaml 
2017-04-22 11:34:30,879 (playbook) [INFO] {"name": "Hello world"}
{'msg': 'Success', 'failed': False, 'stdout': u'"Hello world!"\n', 'stderr': u'', 'exitcode': 0}
2017-04-22 11:34:30,946 (playbook) [INFO] {"name": "Get the list of hosts"}
{'msg': 'Success', 'failed': False, 'stdout': u'127.0.0.1\tlocalhost\n# The following lines are desirable for IPv6 capable hosts\n::1     ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters\n', 'stderr': u'', 'exitcode': 0}

```