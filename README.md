# helix-swarm

![Tests](https://github.com/pbelskiy/helix-swarm/workflows/Tests/badge.svg)
![Coveralls github](https://img.shields.io/coveralls/github/pbelskiy/helix-swarm?label=Coverage)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/helix-swarm?label=Python)
![PyPI - Downloads](https://img.shields.io/pypi/dm/helix-swarm?color=1&label=Downloads)

Python client for Perforce Helix Swarm (review board)

## Installation

```sh
pip3 install helix-swarm
```
## Usage

There is same API interface for sync and async client versions, underhood it uses
`requests` and `asyncio` respectively. Also you must select REST API version you
want yo use in host url like: `http://server/api/v9`

## Examples

Get review info:
```python
import helixswarm

client = SwarmClient('http://server/api/v9', 'login', 'password')
review = client.reviews.get(12345)
print(review['review']['author'])
```

Add comment to review (async):
```python
import asyncio
import helixswarm

client = SwarmAsyncClient('http://server/api/v5', 'login', 'password')

async def example():
    await client.comments.add('reviews/12345', 'my awesome comment')

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(example())
finally:
    loop.run_until_complete(client.close())
    loop.close()
```

[__Please look at tests directory for more examples.__](https://github.com/pbelskiy/helix-swarm/tree/master/tests)

## Testing

Prerequisites: `tox`

Then just run tox, all dependencies and checks will run automatically
```sh
tox
```

## Contributing

Feel free to any contributions

## Official REST API documentation:

https://www.perforce.com/manuals/swarm/Content/Swarm/swarm-apidoc.html

| Version                                                                                     | Date               | Notes                                                                       |
|:--------------------------------------------------------------------------------------------|:-------------------|:----------------------------------------------------------------------------|
| [v10](https://www.perforce.com/manuals/swarm/Content/Swarm/swarm-apidoc_endpoints-v10.html) | October 2019       | Integration with CI tools                                                   |
| [v9](https://www.perforce.com/manuals/v19.1/swarm/Content/Swarm/swarm-apidoc.html)          | April 2018         | Review append and replace changelist, 2fa, mark comment as read             |
| [v8](https://www.perforce.com/manuals/v17.4/swarm/#Swarm/swarm-apidoc.html)                 | December 2017      | Default reviewers                                                           |
| [v7](https://www.perforce.com/manuals/v17.3/swarm/index.html#Swarm/swarm-apidoc.html)       | October 2017       | Groups as review participants, groups as moderators of project              |
| [v6](https://www.perforce.com/manuals/v17.2/swarm/api.html)                                 | May 2017           | Activity dashboard, archiving reviews, cleaning reviews, for voting reviews |
| v5                                                                                          | October 2016       | Limiting comments to a specific review version                              |
| [v4](https://www.perforce.com/perforce/r16.2/manuals/swarm/api.html)                        | October 2016       | Private projects, file-level and line-level inline comments                 |
| v3                                                                                          | September 2016     | Comments management                                                         |
| [v2](https://www.perforce.com/perforce/r16.1/manuals/swarm/api.html)                        | May 2016           | Projects, groups                                                            |
| [v1.2](https://www.perforce.com/perforce/r15.3/manuals/swarm/api.html)                      | October 2015       | Author filter to the list reviews endpoint                                  |
| [v1.1](https://www.perforce.com/perforce/r14.4/manuals/swarm/api.html)                      | January 2015       | Required reviewers                                                          |
| [v1](https://www.perforce.com/perforce/r14.3/manuals/swarm/api.html)                        | July 2014          | Initial                                                                     |
