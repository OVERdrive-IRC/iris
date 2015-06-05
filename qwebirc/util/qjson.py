import json

__SEPS = (',', ':')
dumps = lambda x: json.dumps(
    x, encoding="utf8", ensure_ascii=True, check_circular=False, indent=None, separators=__SEPS)
loads = lambda x: json.loads(x, encoding="utf8")
