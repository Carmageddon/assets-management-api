def evaluate_condition(asset, condition):
    def match_tag_condition(tags, condition_tags):
        tags_dict = {tag['key']: tag['value'] for tag in tags}
        for cond_tag in condition_tags:
            if tags_dict.get(cond_tag['key']) != cond_tag['value']:
                return False
        return True

    for key, value in condition.items():
        if key == "AND":
            if not all(evaluate_condition(asset, sub_condition) for sub_condition in value):
                return False
        elif key == "OR":
            if not any(evaluate_condition(asset, sub_condition) for sub_condition in value):
                return False
        elif key == "tags":
            if not match_tag_condition(asset.get('tags', []), value):
                return False
        elif key.endswith("_contains"):
            field = key[:-9]  # Remove '_contains' from the key
            if field in asset:
                if value not in asset[field]:
                    return False
            else:
                return False
        else:
            parts = key.split('.')
            d = asset
            for part in parts:
                if part in d:
                    d = d[part]
                else:
                    return False
            if d != value:
                return False
    return True
