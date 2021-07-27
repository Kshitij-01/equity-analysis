import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')
page_py = wiki_wiki.page('Reliance Industries')
# print("hello", page_py.summary[0:])

wiki_html = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.HTML
)
p_html = wiki_html.page("Reliance Industries")

print(p_html.text[:p_html.text.find('See also')-4])