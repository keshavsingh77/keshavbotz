from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name='MovieBot')

def create_telegraph_page(title, content):
    page = telegraph.create_page(title, html_content=content)
    return f"https://telegra.ph/{page['path']}"
