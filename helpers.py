from math import ceil


def pagination(page, total_count, per_page):
    pagination = {}
    pagination['previous_page'] = page - 1
    if not pagination['previous_page']:
        pagination['previous_page'] = None

    pagination['current_page'] = page

    pagination['next_page'] = None

    pages_count = ceil(float(total_count)/per_page)

    if pages_count > page:
        pagination['next_page'] = page + 1

    return pagination
