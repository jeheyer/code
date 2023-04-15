import math

def GetColumn(matrix, column_n):
    return [row[column_n] for row in matrix]

def GetPaymentData(options = {}):

    from datetime import date
    today = date.today()

    # Fill in default values if field was not provided
    #default_values = dict(loanAmount = 200000, years = 30, interestRate = 3.25, startYear = today.year, startMonth = today.month)
    #for key, default_value in default_values.items():
    #    if not key in options:
    #        options[key] = default_value

    loanAmount = int(options.get('loanAmount', 200000))
    years = int(options.get('years', 30))
    interestRate = float(options.get('interestRate', 3.25))
    startYear = int(options.get('startYear', today.year))
    startMonth = int(options.get('startMonth', today.month))

    # Loan duration (in months)
    numberOfPayments = years * 12

    data = dict(loanAmount = loanAmount, years = years, startYear = startYear, startMonth = startMonth, numberOfPayments = numberOfPayments, interestRate = interestRate)

    # Calculate overall loan stuff
    c = interestRate / 1200
    monthlyPayment = round(loanAmount * (c * ((1 + c) ** numberOfPayments)) / (((1 + c) ** numberOfPayments) - 1), 2)
    sumOfPayments = round(monthlyPayment * numberOfPayments, 2)
    sumOfInterestPayments = sumOfPayments - loanAmount
    data.update(dict(monthlyPayment = monthlyPayment, sumOfPayments = sumOfPayments, sumOfInterestPayments = sumOfInterestPayments))

    year = startYear
    payments = []; paymentBreakdown = []; remainingBalances = []
    remainingBalances.append(loanAmount)

    for y in range(0, years + 1):

        if y == 0:
            # Fill first year in with zeros
            for _ in range(1, startMonth):
                payments.append([0, 0, 0])
            cal_month = startMonth
        else:
            cal_month = 1

        for cal_month in range(cal_month, 13):

            loanMonth = (y * 12) + (cal_month - startMonth) + 1

            if loanMonth <= numberOfPayments:
                remainingBalance = round(loanAmount * (((c + 1) ** numberOfPayments) - ((c + 1) ** loanMonth)) / (
                            ((c + 1) ** numberOfPayments) - 1), 2)
                principle = round((sum(remainingBalances[-1:]) - remainingBalance), 2)               
                interest = round(monthlyPayment - principle, 2)
                payments.append([monthlyPayment, principle, interest])
                remainingBalances.append(round(remainingBalance, 2))

        if y == 0:
            start_index = startMonth - 1
            end_index = 12
        else:
            start_index = 12 * y
            if y >= years:
                end_index = loanMonth + startMonth
            else:
                end_index = start_index + 12

        # Wrap up year data
        y_data = {'calendarYear': year}
        fields = ['paymentsInYear', 'principleInYear', 'interestInYear']
        for i, field in enumerate(fields):
            y_data.update({field: round(sum(GetColumn(payments[start_index:end_index], i)), 2)})

        y_data.update({'remainingBalance': round(sum(remainingBalances[-1:]), 2)})
        y_data.update({'sumOfPrinciple': round(sum(GetColumn(payments, 1), 2))})
        y_data.update({'sumOfInterestPayments': round(sum(GetColumn(payments, 2), 2))})
        paymentBreakdown.append(y_data)
        year += 1

    # Final summary
    data.update({'paymentBreakdown': paymentBreakdown})
    fields = ['sumOfPayments', 'sumOfPrinciple', 'sumOfInterestPayments']
    for i, field in enumerate(fields):
        data.update({field: round(sum(GetColumn(payments, i)), 2)})

    return data
