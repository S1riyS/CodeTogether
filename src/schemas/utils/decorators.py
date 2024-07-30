from pydantic import BaseModel, create_model


def omit(*fields):
    """Omit pydantic fields from model"""

    def dec(_class: BaseModel):
        for field in fields:
            _class.model_fields.pop(field, None)
        _clone = create_model(
            _class.__name__,
            __config__=_class.model_config,
            **{k: (v.annotation, v) for k, v in _class.model_fields.items()},
        )
        setattr(_clone, "__pydantic_parent_namespace__", {})
        return _clone

    return dec
