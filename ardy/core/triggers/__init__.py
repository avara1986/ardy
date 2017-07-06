from importlib import import_module


def get_trigger(trigger, lambda_conf, lambda_function_arn):
    driver_module = 'ardy.core.triggers.{}'.format(trigger)
    try:
        module = import_module(driver_module)
    except ImportError:
        raise ImportError('No trigger for {}'.format(trigger))
    else:
        return module.Driver(lambda_conf=lambda_conf, lambda_function_arn=lambda_function_arn)
