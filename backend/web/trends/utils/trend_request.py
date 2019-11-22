from flask import abort


def parameter_to_int(param, param_name):
    try:
        param = int(param)
        if param <= 0:
            abort(400, "Parameter {} should be positive integer".format(param_name))
    except ValueError as e:
        abort(400, "Parameter {} should be positive integer".format(param_name))
    return param


def handle_videos_request(request):
    tag = request.args.get('tag')

    if tag == "":
        tag = None

    num_docs = request.args.get('num_docs')
    if num_docs is None:
        num_docs = 20

    num_docs = parameter_to_int(num_docs, 'num_docs')

    period = request.args.get('period')
    if period is None:
        period = 1

    period = parameter_to_int(period, 'period')

    return tag, num_docs, period


def handle_trends_request(request):

    tag, num_docs, period = handle_videos_request(request)

    source = request.args.get('source')
    if source is None or source == '':
        source = 'mixed'

    if source not in ('mixed', 'google', 'efir'):
        abort(400, "Parameter source should be 'efir', 'google' or empty (for mixed query)")

    return tag, num_docs, period, source
