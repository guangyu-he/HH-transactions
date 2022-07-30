def header_cases(header: str, file_name: str = ""):
    """

    :param header: text from header
    :param file_name: name of the file
    :return: the column title
    """
    cases_list = [
        {
            "case_name": "Date",
            "case_situation": [
                "date" in header.lower() and "Mandate" not in header,
                "datum" in header.lower()
            ]
        },
        {
            "case_name": "Payee",
            "case_situation": [
                "Beneficiary / Originator" in header,
                "Payee" in header,
                "Beschreibung" in header,
                "Memo" in header
            ]
        },
        {
            "case_name": "Amount",
            "case_situation": [
                "Amount (EUR)" in header,
                "Debit" in header,
                "Betrag" in header,
                "Amount" in header and "cash" in file_name  #
            ]
        },
        {
            # Only DB has credit column
            "case_name": "Credit",
            "case_situation": [
                "Credit" in header
            ]
        }
    ]

    for each_item in cases_list:
        if any(each_item["case_situation"]):
            return each_item["case_name"]
