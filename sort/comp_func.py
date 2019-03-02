"""."""


def cmp_func(num_a, num_b, is_descend=False):
    """默认 < """
    if is_descend:
        return (num_a > num_b)
    else:
        return (num_a < num_b)
