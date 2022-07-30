def case_result(str_each_row: str):
    """
    categorize transactions

    :param str_each_row: each transaction row
    :return: category
    """

    cases_list = [
        {
            "case_name": "Fitness",
            "case_situation":
                ["Fitness" in str_each_row]
        },
        {
            "case_name": "Restaurant",
            "case_situation":
                [
                    "SumUp" in str_each_row,
                    "RESTAURANT" in str_each_row.upper() and "MCDONALDS" not in str_each_row,
                    "China Rest. Sonne" in str_each_row,
                    "Food" in str_each_row and "cash" in str_each_row.lower(),  # food item in cash.csv
                ]
        },
        {
            "case_name": "Entertain",
            "case_situation":
                [
                    "CINESTAR" in str_each_row,
                    "MAKERY" in str_each_row
                ]
        },
        {
            "case_name": "Insurance",
            "case_situation":
                [
                    "Barmenia" in str_each_row,
                    "HANSEMERKUR" in str_each_row,
                    "WERTGARANTIE" in str_each_row
                ]
        },
        {

            "case_name": "Grocery",
            "case_situation":
                [
                    "REWE" in str_each_row,
                    "DM" in str_each_row,
                    "Lidl" in str_each_row,
                    "APOTHEKE" in str_each_row,
                    "MUJI" in str_each_row,
                    "Orient Master" in str_each_row
                ]

        },
        {

            "case_name": "Fast-Food",
            "case_situation":
                [
                    "AmRest" in str_each_row,
                    "MCDONALDS" in str_each_row,
                    "Curry Wolf " in str_each_row
                ]
        },
        {

            "case_name": "Clothing",
            "case_situation":
                [
                    "OTHERSTORIE" in str_each_row,
                    "UNIQLO" in str_each_row,
                    "ARKET" in str_each_row,
                    "ACE & TATE" in str_each_row,
                    "VANS" in str_each_row,
                    "PUNTOFASLMA" in str_each_row,
                    "DECATHLON" in str_each_row,
                    "UNDERARMOUR" in str_each_row,
                    "NIKE" in str_each_row
                ]
        },
        {

            "case_name": "Online-Shopping",
            "case_situation":
                [
                    "ESTEELAUDER" in str_each_row,
                    "AMAZON" in str_each_row
                ]
        },
        {

            "case_name": "Abo",
            "case_situation":
                [
                    "DIGITALRIVE" in str_each_row,
                    "VULTR" in str_each_row
                ]
        },
        {
            "case_name": "Apple",
            "case_situation": [
                "APPLE" in str_each_row
            ]
        },
        {
            "case_name": "Telekom",
            "case_situation": [
                "Telekom" in str_each_row
            ]
        },
        {
            "case_name": "Electronics",
            "case_situation": [
                "MEDIA MARKT" in str_each_row,
                "SATURN" in str_each_row
            ]
        },
        {
            "case_name": "Takeout",
            "case_situation": [
                "PayPal Europe S.a.r.l. et Cie S.C.A" in str_each_row and "FR7630004021180001013711792" in str_each_row
            ]
        },
        {
            "case_name": "Storm",
            "case_situation": [
                "VATTENFALL" in str_each_row
            ]
        },
        {
            "case_name": "Transportation",
            "case_situation": [
                "BVG" in str_each_row
            ]
        }
    ]

    for each_item in cases_list:
        if any(each_item["case_situation"]):
            return each_item["case_name"]
