def my_func(**kwargs):
    """
    示例函数

    Args:
      **kwargs: 不定长度的关键字参数

    Returns:
      None
    """
    print(kwargs)
    for k, v in kwargs.items():
        print(f'{k} = {v}')


if __name__ == '__main__':
    my_func(name="John", age=30)
