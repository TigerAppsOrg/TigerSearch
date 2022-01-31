def email_url(netid, item_title, is_found_post, mobile):
    if mobile:
        url = f"mailto:{netid}@princeton.edu?subject=TigerSearch: {item_title}&body="
    else:
        url = f"https://mail.google.com/mail/?extsrc=mailto&url=mailto%3A%3Fto%3D{netid}%40princeton.edu%26subject%3DTigerSearch:%2520{item_title}%26body%3D"

    if(is_found_post):
        url += (f"Hello,%0d%0a%0d%0aI think the %22{item_title}%22 that you listed "
                "on TigerSearch may belong to me.%0d%0aPlease let me know when you're "
                "available to meet up and exchange the item."
                "%0d%0a%0d%0aNote from the TigerSearch Team to the poster: Please follow this link to resolve your "
                "post on TigerSearch after returning the item:%0d%0ahttps://search.tigerapps.org/myposts"
                "%0d%0a%0d%0aThank you")

    else:
        url += (f"Hello,%0d%0a%0d%0aI think I've found the %22{item_title}%22 that "
                "you listed on TigerSearch.%0d%0aPlease let me know when you're "
                "available to meet up and exchange the item."
                "%0d%0a%0d%0aNote from the TigerSearch team to the poster: Please follow this link to resolve your "
                "post on TigerSearch after receiving the item:%0d%0ahttps://search.tigerapps.org/myposts"
                "%0d%0a%0d%0aThank you")

    return url
    # https://mail.google.com/mail/?extsrc=mailto&url=mailto%3A%3Fto%3Dsomeguy%40gmail.com%26subject%3DHi%2520There%26body%3Dbody%2520goes%2520here
    #
