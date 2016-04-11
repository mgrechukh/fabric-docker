Compose file may be specified with env:

```
fab --set compose_file=preproduction.yml do:ps
```

Alternatively, in command parameters:

```
fab do:ps,config=preproduction.yml

```

```
fab do:scale,batch_worker=2,web=5,config=preproduction.yml

```

Pull and up -d:

```
fab do:pullup,batch_worker,config=preproduction.yml

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

Parameters passed to compose will include both configuration files in correct order. And staging will use another machine.
