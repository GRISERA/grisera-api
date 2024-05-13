def prepare_links(route):
    """
    Prepare list of links for given route differing by its request methods

    Args:
        route (Route): Route for which links are prepared

    Returns:
        List of links for given route
    """
    return list(map(lambda method: {'rel': route.name, '$ref': route.path, 'action': method}, route.methods))


def get_links(router):
    """
    Return list of links from given router

    Args:
        router (Router): Router to get links from

    Returns:
        List of links
    """
    return sum(list(map(prepare_links, router.routes)), [])
