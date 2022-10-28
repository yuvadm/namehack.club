# Domain Name Hack Club

An exclusive club of nerds that own the domain hack to their name.

## Criteria

- Own the [domain hack](https://en.wikipedia.org/wiki/Domain_hack) for your name, e.g. [https://yuv.al](https://yuv.al)
- Serve an active **personal** homepage from that domain, both naked and subdomains (such as `www.`) are allowed

## Join the club

Open a new pull request to this repository that adds a new YAML file to the [`names`](names) directory.

If your domain name is `examp.le` the file name should be `example.yml`, and the following minimal fields are required:

```yaml
domain: examp.le
name: Example Foo
```

Other optional fields are supported:

```yaml
domain: examp.le
name: Example Foo
url: https://examp.le/about/ # use to specify homepage URL, defaults to https://examp.le
title: UI/UX designer # maximum 80 chars
email: hi@examp.le
```

## Development

Local development requires a basic Python environment with [pipenv](https://pipenv.pypa.io/en/latest/) installed.

```bash
$ pipenv sync --dev
$ pipenv run build
$ pipenv run serve
```
