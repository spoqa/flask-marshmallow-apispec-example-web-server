from typeguard import typechecked


@typechecked
def camelcase(s: str) -> str:
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)
