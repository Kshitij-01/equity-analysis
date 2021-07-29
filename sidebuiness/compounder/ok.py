import locale

locale.setlocale(locale.LC_ALL, locale.getlocale())
dollar_exchange_rate = 4.39
dollar_exchange = 74


def compound_interest(principle, rate, time):
    Amount = principle * (pow((1 + rate / 100), time))
    CI = Amount - principle
    return Amount


while True:
    invested, s, doll, fer = 0, 0, 0, 0
    initial_dep = int(input('enter initial deposit in rupees'))
    ratee = float(input('enter rate of interest'))
    years = int(input('enter no of years'))
    dollar = input('enter d for dollar else enter r for rupees')
    m_fromini = compound_interest(initial_dep, ratee, years)
    if dollar == 'd':
        retire = int(input('enter no of years you wanna retire after'))
        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
        monthly_invest = int(input('enter monthly savings in dollars'))
        rate = float(input('enter rate'))
        inflation = float(input('enter inflation rate'))
        for x in range(1, years * 12 + 1):
            invested += monthly_invest + invested * rate / (100 * 12) if x != 1 else monthly_invest
            if x % 12 == 0:
                if x / 12 == 5:
                    print('you got promoted so added $', int(monthly_invest * 0.7), 'as monthly')
                    monthly_invest += monthly_invest * 0.6
                elif x / 12 == 9:
                    print('you got promoted so added $', int(monthly_invest * 0.5), 'as monthly')
                    monthly_invest += monthly_invest * 0.4
                elif x / 12 == 13:
                    print('you got promoted so added $', int(monthly_invest * 0.3), 'as monthly')
                    monthly_invest += monthly_invest * 0.3
                elif x / 12 == retire:
                    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
                    print('your money earned in dollars is ${}'.format(
                        locale.format_string("%d", invested, grouping=True)), end=' ')
                    locale.setlocale(locale.LC_ALL, ('English_India', '1252'))
                    print('  ₹{}'.format(locale.format_string("%d", invested * compound_interest(dollar_exchange,
                                                                                                 dollar_exchange_rate,
                                                                                                 int(x / 12)),
                                                              grouping=True)))
                    print('your money from intial investment in rupees is ₹{}'.format(
                        locale.format_string("%d", compound_interest(initial_dep, ratee, retire), grouping=True)))
                    print('your total networth is ₹{}'.format(
                        locale.format_string("%d", invested * compound_interest(dollar_exchange,
                                                                                dollar_exchange_rate,
                                                                                int(x / 12)) + compound_interest(
                            initial_dep, ratee, retire), grouping=True)))
                    spend = int(input('enter the money you will spend per year in dollars'))
                    inflation = float(input('enter inflation in withdrawals'))
                    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
                    spendd = locale.format_string("%d", spend, grouping=True)
                    locale.setlocale(locale.LC_ALL, ('English_India', '1252'))
                    spendr = locale.format_string("%d", spend * compound_interest(dollar_exchange, dollar_exchange_rate,
                                                                                  retire), grouping=True)
                    print('you got retired and started spending ${}k a year that is ₹{}'.format(spendd, spendr))
                    monthly_invest = -spend / 12
                else:
                    monthly_invest += monthly_invest * inflation / 100
                locale.setlocale(locale.LC_ALL, 'en_US.utf8')
                print('year', int(x / 12), "  ${}".format(locale.format_string("%d", invested, grouping=True)), end=' ')
                locale.setlocale(locale.LC_ALL, ('English_India', '1252'))
                print('  ₹{}'.format(locale.format_string("%d", invested * compound_interest(dollar_exchange,
                                                                                             dollar_exchange_rate,
                                                                                             int(x / 12)),
                                                          grouping=True)))
        fer = compound_interest(dollar_exchange, dollar_exchange_rate, years)
        s = invested * fer
        print('money earned in U.S.A in rupees is ₹', locale.format_string("%d", s, grouping=True))
        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
        doll = locale.format_string("%d", invested, grouping=True)
        print('yearly investments in U.S.A final is $', locale.format_string("%d", monthly_invest * 12, grouping=True))
        print('money in U.S.A in dollars is $', doll)
    else:
        retire = int(input('enter no of years you wanna retire after'))
        monthly_invest = int(input('enter monthly savings in rupees'))
        rate = float(input('enter rate'))
        inflation = float(input('enter inflation rate'))
        for x in range(1, years * 12 + 1):
            invested += monthly_invest + invested * rate / (100 * 12) if x != 1 else monthly_invest
            if x % 12 == 0:
                if x / 12 == 5:
                    print('you got promoted so added ₹', int(monthly_invest * 0.7), 'as monthly')
                    monthly_invest += monthly_invest * 1
                elif x / 12 == 9:
                    print('you got promoted so added ₹', int(monthly_invest * 0.5), 'as monthly')
                    monthly_invest += monthly_invest * 0.8
                elif x / 12 == 13:
                    print('you got promoted so added ₹', int(monthly_invest * 0.3), 'as monthly')
                    monthly_invest += monthly_invest * 0.4
                    print('last promotion makes monthly investment as',
                          locale.format_string("%d", monthly_invest, grouping=True))
                elif x / 12 == retire:
                    locale.setlocale(locale.LC_ALL, ('English_India', '1252'))
                    print('your money earned in rupees is ₹{}'.format(
                        locale.format_string("%d", invested, grouping=True)))
                    print('your money from intial investment in rupees is ₹{}'.format(
                        locale.format_string("%d", compound_interest(initial_dep, ratee, retire), grouping=True)))
                    print('your total networth is ₹{}'.format(
                        locale.format_string("%d", invested + compound_interest(initial_dep, ratee, retire),
                                             grouping=True)))
                    spend = int(input('enter the money you will spend per year in rupees '))
                    inflation = float(input('enter inflation in withdrawals'))
                    spendr = locale.format_string("%d", spend, grouping=True)
                    print('you got retired and started spending ₹{} yearly'.format(spendr))
                    monthly_invest = -spend / 12
                else:
                    monthly_invest += monthly_invest * inflation / 100
                locale.setlocale(locale.LC_ALL, ('English_India', '1252'))
                print('year', int(x / 12),
                      '  ₹{}'.format(locale.format_string("%d", invested,
                                                          grouping=True)))
        s = invested
        print('yearly investments in INDIA final is ₹', locale.format_string("%d", monthly_invest * 12, grouping=True))
    final_amount = s + m_fromini
    locale.setlocale(locale.LC_ALL, ('English_India', '1252'))
    d, v, flag = 10000000, 'C.r', False
    if final_amount < 10000000 and m_fromini < 10000000:
        d, v = 100000, 'Lac'
    if s // d == 0:
        flag = True
    print('final Net worth is ₹', locale.format_string("%d", final_amount // d, grouping=True),
          '{}\nmoney from initial investments ₹'.format(v),
          locale.format_string("%d", m_fromini // d, grouping=True), '{}\nmoney earned by myself ₹'.format(v),
          locale.format_string("%d", s // d if s // d != 0 else s // 100000, grouping=True),
          '{}\nfuture exchange rate ₹'.format(v if not flag else 'Lac'), fer)
