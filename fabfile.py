from fabric.api import env, local, prefix, settings, hide
from fabric.utils import abort
import fabric.colors

def parse(compose_file):
	options = {}
	known_prefix = '# @satelliz-'
	with open(compose_file) as f:
		for line in f:
			if not line.startswith(known_prefix):
				continue
			name, sep, value = line.partition(': ')
			if not sep or not value or not str(value).strip():
				continue
			name = name[len(known_prefix):]
			options[name] = value.strip()
	return options

def get_machine_env(machine):
	if machine.startswith('swarm@'):
		machine = '--swarm ' + machine[6:]

	with settings(warn_only=True),hide("running"):
		_env = local("docker-machine env %s" % machine, capture = True)
	if _env.succeeded:
		return filter(lambda x: x and not x.startswith('#'), _env.stdout.splitlines())
	else:
		fabric.utils.abort(_env.stderr)

def docker_machine(machine):
	docker_env = get_machine_env('-u') # just assure we are not going to break something sensitive
	if machine:
		machine_env = get_machine_env(machine)
		docker_env += machine_env

	cmd_env = " && ".join(docker_env)

	with prefix(cmd_env), hide('running'):
		own_name = local("docker info | grep ^Name | awk '{print $2}'", capture = True)
	print fabric.colors.yellow("-- working on %s (%s)" % (own_name, machine))
	print

	return prefix(cmd_env)

def _merge(x): return " " + " ".join(x) if x else ''

def _prefix(pref, x):
	return pref + _merge(x)

def _prefix_each(pref, x):
	return _merge(["%s %s" % (pref, i) for i in x])

def run_compose(*commands):
	target = env.get('compose_file')
	machine = env.get('docker_machine')

	options = parse(target)
	if not machine and 'use-docker-machine' in options:
		machine = options['use-docker-machine']

	compose_files = [ target, ]
	if 'use-override' in options:
		compose_files.insert(0, options['use-override'])

	compose_prefix = "docker-compose" + _prefix_each('-f', compose_files)

	with docker_machine(machine):
		for c in commands:
			local(compose_prefix + ' ' + c)

def do(*args, **kwargs):
	if 'config' in kwargs:
		env['compose_file'] = kwargs['config']
		del kwargs['config']
	if 'machine' in kwargs:
		env['docker_machine'] = kwargs['machine']
		del kwargs['machine']

	if kwargs:
		args = list(args) + map(lambda x: "%s=%s" % x, kwargs.iteritems())

	if args[0] == 'pullup': # let define combos!
		args = args[1:]
		run_compose(_prefix('pull', args), _prefix('up -d', args))

	elif args[0] == 'drop': # subcommand 'down' works for the whole project only
		args = args[1:]
		run_compose(_prefix('kill', args), _prefix('rm -f', args))

	else:
		run_compose(_merge(args))
