import pytest
import functions as function

driver=None
@pytest.mark.parametrize("town",
                        [
                            "Milford%C2%A0%C2%A0",
                            "Trumbull",
                            "Norwalk",
                            "Stamford",
                            "Shelton",
                            "Fairfield",
                        ]
                        )

# Test case to view all the sales details which is within 7 days
def test_sales_details(town):
    url = function.get_url(town)
    soup = function.create_soup(url)
    flag = 0
    try:
        containers = soup.find("table", {"id": "ctl00_cphBody_GridView1"}).tbody
        index = 1
        while index != 0:
            try:
                row = containers.contents[index]
                days = function.sale_date_difference(row)
                index += 1
                if (days >= 0) and (days <= 7):
                    function.view_notice(row)
            except:
                index = 0
    except:
        flag = 1

    assert flag==0, "City is not available in the list"
