def logout(page):
    page.session.clear()
    page.go("/")
    page.update()