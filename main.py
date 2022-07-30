import os
import pandas as pd
import datetime

from fnmatch import fnmatchcase as match

from payee_cases import case_result
from header_cases import header_cases


def read_sheet(file_name: str):
    list_of_data = [["Date", "Amount", "PayMethod", "CardHolder", "Payee", "Category"]]  # initial header

    """
    pd read csv
    """
    if "Umsätze" in file_name or "sisi_bank" in file_name:
        # some documents are sep by ";"
        df = pd.read_csv(file_name, sep=';')
    else:
        df = pd.read_csv(file_name, on_bad_lines='skip')

    """
    extract table value and header
    """
    if "632" in file_name:
        # Deutsch Bank transaction documents
        table = df.values.tolist()
        for i in range(0, len(table)):
            table[i] = table[i][0].split(";")
        table_header = table[0]
    else:
        table = df.values.tolist()
        table_header = pd.read_csv(file_name, nrows=1).columns.tolist()
        if "Umsätze" in file_name or "sisi_bank" in file_name:
            table_header = table_header[0].split(";")

    """
    analyze the header and try to locate interesting columns
    """
    prefix_header_index = {"Date": -1, "Amount": -1, "Payee": -1, "Credit": -1}
    if table_header is not None and table_header != []:
        for i in range(0, len(table_header)):
            prefix_header_index[header_cases(table_header[i], file_name)] = i

    """
    extract transaction from document
    """
    for each_row in table:

        str_each_row = "".join(str(each_row))  # join and strify each row for convenience

        new_list_data = [""] * 6  # initial the list container

        """
        assign account and holder accroding to the file name
        """
        if "activity" in file_name:
            # amex transaction document
            if "ZAHLUNG/ÜBERWEISUNG" in str_each_row:
                # amex gutschrift
                continue
            else:
                new_list_data[2] = "Amex"
                new_list_data[3] = "Sisi"

        elif "n26_guangyu" in file_name:
            # Guangyu's N26 transaction document
            if "SISI HUANG" in str_each_row.upper() or "GUANGYU HE" in str_each_row.upper():
                # inner transaction
                continue
            else:
                new_list_data[2] = "N26"
                new_list_data[3] = "Guangyu"

        elif "632" in file_name:
            # Guangyu's Deutsche Bank transaction document
            if "SISI HUANG" in str_each_row.upper() or "GUANGYU HE" in str_each_row.upper():
                # inner transaction
                continue
            elif "Golden-Tech" in str_each_row:
                # salary
                continue
            else:
                new_list_data[2] = "DB"
                new_list_data[3] = "Guangyu"

        elif "cash" in file_name:
            # processing cash transaction from APP
            new_list_data[2] = "Cash"

        elif "Umsätze" in file_name:
            # Sisi's barkley account
            if "Gutschrift" in str_each_row:
                # credit card Gutschrift
                continue
            else:
                new_list_data[2] = "Barkley"
                new_list_data[3] = "Sisi"

        elif "n26_sisi" in file_name:
            if "Guangyu" in str_each_row:
                # inner transactions
                continue
            elif match(str_each_row, "*From * to *"):
                # inner transactions
                continue
            elif "American Express" in str_each_row or "BARCLAYS" in str_each_row:
                # inner transactions
                continue
            elif "Raisin DS GmbH" in str_each_row:
                # salary
                continue
            else:
                new_list_data[2] = "N26"
                new_list_data[3] = "Sisi"

        elif "sisi_bank" in file_name:
            # sisi's Commerzbank
            # TODO! need to change in the future
            new_list_data[2] = "Commerz"
            new_list_data[3] = "Sisi"

        """
        get transactions categorized
        """
        new_list_data[5] = case_result(str_each_row)

        """
        get date of transaction 
        """
        if prefix_header_index["Date"] != -1:
            # date column is found in header
            date_in_row = each_row[prefix_header_index["Date"]]
            if "632" in file_name and "date" in date_in_row:
                # should be the header line in DB transaction
                continue
            else:
                new_list_data[0] = date_in_row

        """
        get amount of transactions
        """
        if prefix_header_index["Amount"] != -1:
            # amount column is found in header
            amount_in_row = each_row[prefix_header_index["Amount"]]
            if amount_in_row == "" or amount_in_row == "nan":
                if prefix_header_index["Credit"] != -1:
                    # processing DB Credit column
                    amount_in_row = each_row[prefix_header_index["Credit"]]
                    if amount_in_row == "" or amount_in_row == "nan":
                        continue
                    else:
                        new_list_data[1] = amount_in_row
            else:
                new_list_data[1] = amount_in_row

        """
        get payee of transactions
        """
        if prefix_header_index["Payee"] != -1:
            # amount column is found in header
            payee_in_row = each_row[prefix_header_index["Payee"]]
            if payee_in_row == "" or payee_in_row == "nan":
                continue
            else:
                if "cash" not in payee_in_row.lower() and "cash" in file_name:
                    # transaction without cash flag in cash.csv is discard
                    continue
                else:
                    new_list_data[4] = payee_in_row

        """
        formatting the date from different account
        """
        if new_list_data[2] == "Amex":
            new_list_data[0] = datetime.datetime.strptime(new_list_data[0], "%d/%m/%Y").strftime("%d.%m.%Y")
        elif new_list_data[2] == "N26" or new_list_data[2] == "Cash":
            new_list_data[0] = datetime.datetime.strptime(new_list_data[0], "%Y-%m-%d").strftime("%d.%m.%Y")
        elif new_list_data[2] == "DB":
            new_list_data[0] = datetime.datetime.strptime(new_list_data[0], "%m/%d/%Y").strftime("%d.%m.%Y")
        else:
            pass

        """
        formatting the amount from different account
        """
        if new_list_data[2] == "Amex":
            # well done amex
            pass
        elif new_list_data[2] == "Cash":
            # category the holder in cash.csv from APP
            new_list_data[1] = str(new_list_data[1])
            if "-" in new_list_data[1]:
                new_list_data[3] = "Guangyu"
            else:
                new_list_data[3] = "Sisi"
            new_list_data[1] = new_list_data[1].replace("-", "")
        else:
            # other accounts should switch minus/plus and change to us numerical format
            new_list_data[1] = str(new_list_data[1]).replace(".", ",").replace("€", "").rstrip().lstrip()

            if "-" in str(new_list_data[1]):
                new_list_data[1] = str(new_list_data[1]).replace("-", "")
            else:
                new_list_data[1] = "-" + str(new_list_data[1].replace("+", ""))

        # new_list_data[1] = float(new_list_data[1].replace(",", "."))  # uncomment this line to get a us format table

        """
        append the list as a table
        """
        list_of_data.append(new_list_data)

    return list_of_data[1:]


def main(transactions_folder: str):
    # initial the result list
    result_list = [["Date", "Amount", "PayMethod", "CardHolder", "Payee", "Category"]]

    for path, subdirs, files in os.walk(transactions_folder):
        for name in files:
            if "csv" in name:
                # looking for csv transactions
                return_list = read_sheet(path + "/" + name)
                if return_list is None:
                    print(f"invalid document!")
                else:
                    result_list += return_list

    df = pd.DataFrame(result_list)
    df.to_csv("transaction.csv", header=None, index=None)

    calc_process = input(f"calculate the transaction? yes (y) or no (n):")
    if calc_process == "y":
        sum_guangyu = 0.0
        sum_sisi = 0.0
        sum_guangyu_to_sisi = 0.0
        sum_sisi_to_guangyu = 0.0

        for each_row in result_list[1:]:
            counting_case = [
                each_row[5] == "Restaurant",
                each_row[5] == "Grocery",
                each_row[5] == "Takeout",
                each_row[5] == "Storm"
            ]
            asking_case = [
                each_row[5] == "Clothing",
                each_row[5] == "Online-Shopping",
                each_row[5] == "Electronics",
                each_row[5] == "Entertain",
                each_row[5] == "" and each_row[2] == "Commerz" and "PayPal" in each_row[4],
                # maybe uber eat in sisi's commerzbank
            ]
            if any(counting_case):
                if each_row[3] == "Guangyu":
                    sum_guangyu += float(each_row[1].replace(",", "."))
                elif each_row[3] == "Sisi":
                    sum_sisi += float(each_row[1].replace(",", "."))
                else:
                    # NOTE should not happen
                    pass

            elif any(asking_case):
                while True:
                    answer = input(
                        f"€{each_row[1]} --- {each_row[2]} --- {each_row[4]} @{each_row[0]} "
                        f"is counting (y) or guangyu should pay all (g) or sisi should pay all (s)? or pending (p)?")

                    if answer == "y":
                        if each_row[3] == "Guangyu":
                            sum_guangyu += float(each_row[1].replace(",", "."))
                        elif each_row[3] == "Sisi":
                            sum_sisi += float(each_row[1].replace(",", "."))
                        else:
                            # NOTE should not happen
                            pass
                        break
                    elif answer == "g":
                        if each_row[3] == "Sisi":
                            sum_guangyu_to_sisi += float(each_row[1].replace(",", "."))
                        break
                    elif answer == "s":
                        if each_row[3] == "Guangyu":
                            sum_sisi_to_guangyu += float(each_row[1].replace(",", "."))
                        break
                    elif answer == "p":
                        # usually means there could be refund in the future
                        pass
                    else:
                        print(f"wrong option!")

            else:
                pass

        print(f"Guangyu paid {str(sum_guangyu)}")
        print(f"Sisi paid {str(sum_sisi)}")

        difference = (sum_sisi - sum_guangyu) / 2 + sum_guangyu_to_sisi - sum_sisi_to_guangyu
        if difference > 0:
            print(f"Guangyu should pay Sisi {str(difference)}")
        else:
            print(f"Sisi should pay Guangyu {str(difference)}")

    else:
        pass


if __name__ == "__main__":
    main(f"transactions")
