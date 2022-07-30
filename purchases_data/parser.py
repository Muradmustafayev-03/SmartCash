from requests_html import HTMLSession


def render_JS(fiscal_id):
    session = HTMLSession()
    r = session.get(f'https://monitoring.e-kassa.gov.az/#/index?doc={fiscal_id}')
    r.html.render()
    return r.html.text

print(render_JS("BWN3NBdppgPY"))