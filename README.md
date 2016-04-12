Compose file may be specified with env:

```
fab --set compose_file=preprod.yml do:ps
```

Alternatively, in command parameters:

```
fab do:ps,config=preprod.yml

```

```
fab do:scale,batch_worker=2,web=5,config=preprod.yml

```

Pull and up -d:

```
fab do:pullup,batch_worker,config=preprod.yml

```

Upgrade everything:

```
fab --set compose_file=preprod-staging.yml do:pullup

```

Docker machine specified directly in compose config:


```
# @satelliz-use-docker-machine: swarm@pixar1
```

Compose supports overrides ( https://docs.docker.com/compose/extends/ ). We do also, see preprod-staging.overlay:
```
# @satelliz-use-docker-machine: lumen-dev
# @satelliz-use-override: preprod.yml
```

Parameters passed to compose will include both configuration files in correct order. And also staging will use another machine

And we can use docker directly within machine-environment defined by compose file. We don't even specify it here, since docker-compose.yml used by default:

```
fab do:docker,"ps -a"

```

Or by using wrapper task:

``
fab docker:"ps -a",config=preprod.yml
```

Certain commands not used by compose, so they passed to docker directly without especially asking:

```
fab do:images
```

Again, machine environment still taken from default docker-compose.yml. But we can specify machine directly:


```
fab do:info,machine=swarm@aeterna

```
