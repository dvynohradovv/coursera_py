import unittest

from bs4 import BeautifulSoup


def get_html(path_to_file):
    with open(path_to_file, "r", encoding="utf-8") as fs:
        return fs.read()


def count_htmlimgs(body_content: BeautifulSoup):
    imgs = body_content.find_all("img", width=True)
    # imgs = body_content.select("img[width]")
    quantity = 0
    for img in imgs:
        try:
            if int(img["width"]) >= 200:
                quantity += 1
        except Exception as ex:
            pass
    return quantity


def count_htmlheaders(body_content: BeautifulSoup):
    headers = body_content.find_all([f"h{i}" for i in range(1, 7)])
    quantity = 0
    for h in headers:
        try:
            if h.text[0] in ['E', 'T', 'C']:
                quantity += 1
        except Exception as ex:
            pass
    return quantity


def count_max_sequence_htmllinks(body_content: BeautifulSoup):
    links = body_content("a")
    cur_max = 1
    max = 1
    for i in range(len(links) - 1):
        if links[i].find_next_sibling() is links[i + 1]:
            if links[i].parent is links[i + 1].parent:
                cur_max += 1
        else:
            max = cur_max if cur_max > max else max
            cur_max = 1
    max = cur_max if cur_max > max else max
    return max
    """
    def _get_link_count(links_list):
        max_len = 1
        for i in range(len(links_list)):
            if str(links_list[i])[1] == 'a':
                max_len += 1
            else:
                break
        return max_len

    link_len = 0
    tags = body_content('a')
    for tag in tags:
        tmp_len = _get_link_count(tag.find_next_siblings())
        if tmp_len > link_len:
            link_len = tmp_len
    return link_len
    """


def count_unattached_htmllists(body_content: BeautifulSoup):
    def isunattached(list):
        parents = list.find_parent("li")
        return True if parents is None else False

    html_lists = body_content.find_all(["ul", "ol"])
    quantity = 0
    for list in html_lists:
        quantity += 1 if isunattached(list) else 0
    return quantity


def parse(path_to_file):
    html = get_html(path_to_file)
    bs = BeautifulSoup(html, "lxml")
    body_content = bs.find("div", id="bodyContent")
    imgs = count_htmlimgs(body_content)
    headers = count_htmlheaders(body_content)
    linkslen = count_max_sequence_htmllinks(body_content)
    lists = count_unattached_htmllists(body_content)

    return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    print(parse("wiki/History_of_chess"))
    unittest.main()
